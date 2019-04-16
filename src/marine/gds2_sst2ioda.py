#!/usr/bin/env python

#
# (C) Copyright 2019 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
#

from __future__ import print_function
import argparse
import ioda_conv_ncio as iconv
import netCDF4 as nc
from datetime import datetime, timedelta
import dateutil.parser
import numpy as np
from multiprocessing import Pool
import os


output_var_names = [
    "sea_surface_temperature",
    "sea_surface_skin_temperature"]


def read_input(input_file):
    """
    Reads/converts a single input file, performing optional thinning also.
    In addition to the input argument, the global_config structure needs to
    be populated from outside the functions as well.

    Arguments:

        input_file: The name of file to read

    Returns:

        A tuple of (obs_data, loc_data, attr_data) needed by the IODA writer.
    """
    global global_config

    print("Reading ", input_file)
    ncd = nc.Dataset(input_file, 'r')

    # get the base time (should only have 1 or 2 time slots)
    time_base = ncd.variables['time'][:]
    basetime = dateutil.parser.parse(ncd.variables['time'].units[-20:])

    # get some of the global attributes that we are interested in
    attr_data = {}
    for v in ('platform', 'sensor', 'processing_level'):
        attr_data[v] = ncd.getncattr(v)

    # get the QC flags, and calculate a mask from the non-missing values
    # (since L3 files are mostly empty, fields need a mask applied immediately
    # to avoid using way too much memory)
    data_in = {}
    data_in['quality_level'] = ncd.variables['quality_level'][:].ravel()
    mask = data_in['quality_level'] >= 0
    data_in['quality_level'] = data_in['quality_level'][mask]

    # Determine the lat/lon grid.
    # If L3, we need to convert 1D lat/lon to 2D lat/lon.
    # If len(time) > 1, also need to repeat the lat/lon vals
    lons = ncd.variables['lon'][:].ravel()
    lats = ncd.variables['lat'][:].ravel()
    if attr_data['processing_level'][:2] == 'L3':
        len_grid = len(lons)*len(lats)
        lons, lats = np.meshgrid(lons, lats, copy=False)
        lons = np.tile(lons.ravel(), len(time_base)).ravel()[mask]
        lats = np.tile(lats.ravel(), len(time_base)).ravel()[mask]
    else:
        len_grid = len(lons)
        lons = np.tile(lons, len(time_base)).ravel()[mask]
        lats = np.tile(lats, len(time_base)).ravel()[mask]

    # calculate the basetime offsets
    time = np.tile(np.atleast_2d(time_base).T, (1, len_grid)).ravel()[mask]

    # load in all the other data and apply the missing value mask
    input_vars = (
        'quality_level',
        'sst_dtime',
        'sses_bias',
        'sses_standard_deviation',
        'sea_surface_temperature')
    for v in input_vars:
        if v not in data_in:
            data_in[v] = ncd.variables[v][:].ravel()[mask]
    ncd.close()

    # Create a mask for optional random thinning
    np.random.seed(
        int((global_config['date']-datetime(1970, 1, 1)).total_seconds()))
    mask = np.random.uniform(size=len(lons)) > args.thin

    # also, sometimes certain input variables have their own mask due to
    # missing values
    for v in input_vars:
        if np.ma.is_masked(data_in[v]):
            mask = np.logical_and(mask, np.logical_not(data_in[v].mask))

    # apply the masks for thinning and missing values
    time = time[mask]
    lons = lons[mask]
    lats = lats[mask]
    for v in input_vars:
        data_in[v] = data_in[v][mask]

    # create a string version of the date for each observation
    dates = []
    for i in range(len(lons)):
        obs_date = basetime + \
            timedelta(seconds=float(time[i]+data_in['sst_dtime'][i]))
        dates.append(obs_date.strftime("%Y-%m-%dT%H:%M:%SZ"))

    # calculate output values
    # Note: the qc flags in GDS2.0 run from 0 to 5, with higher numbers
    # being better. IODA typically expects 0 to be good, and higher numbers
    # are bad, so the qc flags flipped here.
    # TODO change everything in soca to handle K instead of C ?
    val_sst_skin = data_in['sea_surface_temperature'] - 273.15
    val_sst = val_sst_skin - data_in['sses_bias']
    err = data_in['sses_standard_deviation']
    qc = 5 - data_in['quality_level']

    # allocate space for output depending on which variables are to be saved
    num_vars = 0
    if global_config['output_sst']:
        num_vars += 1
    if global_config['output_skin_sst']:
        num_vars += 1
    obs_dim = (num_vars, len(lons))
    obs_data = {
        global_config['oval_name']: np.zeros(obs_dim),
        global_config['oerr_name']: np.zeros(obs_dim),
        global_config['opqc_name']: np.zeros(obs_dim),
    }

    # create the final output structures
    loc_data = {
        'latitude': lats,
        'longitude': lons,
        'date_time': dates,
    }
    idx = 0
    if global_config['output_sst']:
        obs_data[global_config['oval_name']][idx, :] = val_sst
        obs_data[global_config['oerr_name']][idx, :] = err
        obs_data[global_config['opqc_name']][idx, :] = qc
        idx += 1
    if global_config['output_skin_sst']:
        obs_data[global_config['oval_name']][idx, :] = val_sst_skin
        obs_data[global_config['oerr_name']][idx, :] = err
        obs_data[global_config['opqc_name']][idx, :] = qc

    return (obs_data, loc_data, attr_data)


###############################################################################
###############################################################################


if __name__ == '__main__':

    # Get command line arguments
    parser = argparse.ArgumentParser(
        description=(
            'Reads the sea surface temperature from any GHRRST Data '
            ' Specification (GDS2.0) formatted L2 or L3 file(s) and converts'
            ' into IODA formatted output files. Multiple files are'
            ' concatenated and optional thinning can be performed.')
    )

    required = parser.add_argument_group(title='required arguments')
    required.add_argument(
        '-i', '--input',
        help="path of GHRSST GDS2.0 SST observation input file(s)",
        type=str, nargs='+', required=True)
    required.add_argument(
        '-o', '--output',
        help="path of IODA output file",
        type=str, required=True)
    required.add_argument(
        '-d', '--date',
        metavar="YYYYMMDDHH",
        help="base date for the center of the window",
        type=str, required=True)

    optional = parser.add_argument_group(title='optional arguments')
    optional.add_argument(
        '-t', '--thin',
        help="percentage of random thinning, from 0.0 to 1.0. Zero indicates"
             " no thinning is performed. (default: %(default)s)",
        type=float, default=0.0)
    optional.add_argument(
        '--threads',
        help='multiple threads can be used to load input files in parallel.'
             ' (default: %(default)s)',
        type=int, default=1)
    optional.add_argument(
        '--sst',
        help='if set, only the bias corrected bulk sst is output.'
             ' Otherwise, bulk sst, and skin sst are both output.',
        action='store_true')
    optional.add_argument(
        '--skin_sst',
        help='if set, only the skin or subskin sst is output.'
             ' Otherwise, bulk sst, and skin sst are both output.',
        action='store_true')

    args = parser.parse_args()
    args.date = datetime.strptime(args.date, '%Y%m%d%H')
    if not args.sst and not args.skin_sst:
        args.sst = True
        args.skin_sst = True

    # setup the IODA writer
    writer = iconv.NcWriter(args.output, [], [])

    # Setup the configuration that is passed to each worker process
    # Note: Pool.map creates separate processes, and so other than the
    # argument array passed in (args.input), it can only read global variables
    global_config = {}
    global_config['date'] = args.date
    global_config['thin'] = args.thin
    global_config['oval_name'] = writer.OvalName()
    global_config['oerr_name'] = writer.OerrName()
    global_config['opqc_name'] = writer.OqcName()
    global_config['output_sst'] = args.sst
    global_config['output_skin_sst'] = args.skin_sst

    # read / process files in parallel
    pool = Pool(args.threads)
    obs = pool.map(read_input, args.input)

    # concatenate the data from the files
    obs_data, loc_data, attr_data = obs[0]
    loc_data['date_time'] = writer.FillNcVector(
        loc_data['date_time'], "datetime")
    for i in range(1, len(obs)):
        for k in obs_data:
            axis = len(obs[i][0][k].shape)-1
            obs_data[k] = np.concatenate(
                (obs_data[k], obs[i][0][k]), axis=axis)
        for k in loc_data:
            d = obs[i][1][k]
            if k == 'date_time':
                d = writer.FillNcVector(d, 'datetime')
            loc_data[k] = np.concatenate((loc_data[k], d), axis=0)

    # prepare global attributes we want to output in the file,
    # in addition to the ones already loaded in from the input file
    attr_data['date_time_string'] = args.date.strftime("%Y-%m-%dT%H:%M:%SZ")
    attr_data['thinning'] = args.thin
    attr_data['converter'] = os.path.basename(__file__)

    # pass parameters to the IODA writer
    # (needed because we are bypassing ExtractObsData within BuildNetcdf)
    writer._nrecs = 1
    writer._nvars = obs_data['ObsValue'].shape[0]
    writer._nlocs = obs_data['ObsValue'].shape[1]
    writer._nobs = writer._nvars * writer._nlocs

    # determine which variables we are going to output
    selected_names = []
    if args.sst:
        selected_names.append(output_var_names[0])
    if args.skin_sst:
        selected_names.append(output_var_names[1])
    var_data = {writer._var_list_name: writer.FillNcVector(
        selected_names, "string")}

    # use the writer class to create the final output file
    writer.WriteNcAttr(attr_data)
    writer.WriteNcObsVars(obs_data, var_data)
    writer.WriteNcMetadata(writer._rec_md_name, writer._nrecs_dim_name, {})
    writer.WriteNcMetadata(writer._loc_md_name,
                           writer._nlocs_dim_name, loc_data)
    writer.WriteNcMetadata(writer._var_md_name,
                           writer._nvars_dim_name, var_data)