# wrfda_ncdiag.py
# a collection of classes, and supporting information
# to read in WRFDA netCDF diagnostic files and rewrite them
# into JEDI UFO GeoVaLs and IODA observation files
###############################################################################
###############################################################################
# dictionaries and lists
# LocKeyList = { 'wrfdaname':[('IODAname','dtype')]}

wrfda_miss_float = -888888.
wrfda_miss_int = -888888

all_LocKeyList = {
    'date': [('datetime', 'string')],
    'lat': [('latitude', 'float')],
    'lon': [('longitude', 'float')],
    'elv': [('height_above_mean_sea_level', 'float')],
    'scanpos': [('scan_position', 'float')],
    'satzen': [('sensor_zenith_angle', 'float'),
               ('sensor_view_angle', 'float')],
    'satazi': [('sensor_azimuth_angle', 'float')],
    'solzen': [('solar_zenith_angle', 'float')],
    'solazi': [('solar_azimuth_angle', 'float')],
    'cloud_frac': [('cloud_area_fraction', 'float')],
}

wrfda_add_vars = {
#    'tb_bak':     'WrfdaHofX',
#    'tb_bak_clr': 'WrfdaHofXClrSky',
    'tb_omb':     'WrfdaOmB',
    'tb_err':     'WrfdaFinalObsError',
#    'cloud_obs':  'WrfdaCloudObs',
#    'cloud_mod':  'WrfdaCloudModel',
}

rad_platform_sensor_combos = [
#    'eos-2-airs',
#    'fy3-1-mwhs',
#    'fy3-1-mwts',
#    'fy3-2-mwhs',
#    'fy3-2-mwts',
#    'fy3-3-mwhs2',
#    'gcom-w-1-amsr2',
    'goes-16-abi',
    'goes-17-abi',
    'himawari-8-ahi',
#    'jpss-0-atms',
#    'metop-1-amsua',
#    'metop-1-iasi',
#    'metop-1-mhs',
#    'metop-2-amsua',
#    'metop-2-iasi',
#    'metop-2-mhs',
#    'msg-2-seviri',
#    'msg-3-seviri',
#    'noaa-15-amsua',
#    'noaa-16-amsua',
#    'noaa-16-amsub',
#    'noaa-17-amsub',
#    'noaa-17-hirs',
#    'noaa-18-amsua',
#    'noaa-18-hirs',
#    'noaa-18-mhs',
#    'noaa-19-amsua',
#    'noaa-19-mhs'
]

sensor_chanlist_dict = {
    'abi': list(range(7,17)),
    'ahi': list(range(7,17)),
#    'airs': [1,6,7,10,11,15,16,17,20,21,22,24,27,28,30,36,39,40,42,51,52,54,55,56,59,62,63,68,69,71,72,73,74,75,76,77,78,79,80,82,83,84,86,92,93,98,99,101,104,105,108,110,111,113,116,117,123,124,128,129,138,139,144,145,150,151,156,157,159,162,165,168,169,170,172,173,174,175,177,179,180,182,185,186,190,192,198,201,204,207,210,215,216,221,226,227,232,252,253,256,257,261,262,267,272,295,299,300,305,310,321,325,333,338,355,362,375,453,475,484,497,528,587,672,787,791,843,870,914,950,1003,1012,1019,1024,1030,1038,1048,1069,1079,1082,1083,1088,1090,1092,1095,1104,1111,1115,1116,1119,1120,1123,1130,1138,1142,1178,1199,1206,1221,1237,1252,1260,1263,1266,1285,1301,1304,1329,1371,1382,1415,1424,1449,1455,1466,1477,1500,1519,1538,1545,1565,1574,1583,1593,1614,1627,1636,1644,1652,1669,1674,1681,1694,1708,1717,1723,1740,1748,1751,1756,1763,1766,1771,1777,1780,1783,1794,1800,1803,1806,1812,1826,1843,1852,1865,1866,1868,1869,1872,1873,1876,1881,1882,1883,1911,1917,1918,1924,1928,1937,1941,2099,2100,2101,2103,2104,2106,2107,2108,2109,2110,2111,2112,2113,2114,2115,2116,2117,2118,2119,2120,2121,2122,2123,2128,2134,2141,2145,2149,2153,2164,2189,2197,2209,2226,2234,2280,2318,2321,2325,2328,2333,2339,2348,2353,2355,2357,2363,2370,2371,2377],
#    'iasi': [16,29,32,35,38,41,44,47,49,50,51,53,55,56,57,59,61,62,63,66,68,70,72,74,76,78,79,81,82,83,84,85,86,87,89,92,93,95,97,99,101,103,104,106,109,110,111,113,116,119,122,125,128,131,133,135,138,141,144,146,148,150,151,154,157,159,160,161,163,167,170,173,176,179,180,185,187,191,193,197,199,200,202,203,205,207,210,212,213,214,217,218,219,222,224,225,226,228,230,231,232,236,237,239,243,246,249,252,254,259,260,262,265,267,269,275,279,282,285,294,296,299,300,303,306,309,313,320,323,326,327,329,332,335,345,347,350,354,356,360,363,366,371,372,373,375,377,379,381,383,386,389,398,401,404,405,407,408,410,411,414,416,418,423,426,428,432,433,434,439,442,445,450,457,459,472,477,483,509,515,546,552,559,566,571,573,578,584,594,625,646,662,668,705,739,756,797,867,906,921,1027,1046,1090,1098,1121,1133,1173,1191,1194,1222,1271,1283,1338,1409,1414,1420,1424,1427,1430,1434,1440,1442,1445,1450,1454,1460,1463,1469,1474,1479,1483,1487,1494,1496,1502,1505,1509,1510,1513,1518,1521,1526,1529,1532,1536,1537,1541,1545,1548,1553,1560,1568,1574,1579,1583,1585,1587,1606,1626,1639,1643,1652,1658,1659,1666,1671,1675,1681,1694,1697,1710,1786,1791,1805,1839,1884,1913,1946,1947,1991,2019,2094,2119,2213,2239,2271,2289,2321,2333,2346,2349,2352,2359,2367,2374,2398,2426,2562,2701,2741,2745,2760,2819,2889,2907,2910,2919,2921,2939,2944,2945,2948,2951,2958,2971,2977,2985,2988,2990,2991,2993,3002,3008,3014,3027,3029,3030,3036,3047,3049,3052,3053,3055,3058,3064,3069,3087,3093,3098,3105,3107,3110,3116,3127,3129,3136,3146,3151,3160,3165,3168,3175,3178,3189,3207,3228,3244,3248,3252,3256,3263,3281,3295,3303,3309,3312,3322,3326,3354,3366,3375,3378,3411,3416,3432,3438,3440,3442,3444,3446,3448,3450,3452,3454,3458,3467,3476,3484,3491,3497,3499,3504,3506,3509,3518,3527,3555,3575,3577,3580,3582,3586,3589,3599,3610,3626,3638,3646,3653,3658,3661,3673,3689,3700,3710,3726,3763,3814,3841,3888,4032,4059,4068,4082,4095,4160,4234,4257,4411,4498,4520,4552,4567,4608,4646,4698,4808,4849,4920,4939,4947,4967,4991,4996,5015,5028,5056,5128,5130,5144,5170,5178,5183,5188,5191,5368,5371,5379,5381,5383,5397,5399,5401,5403,5405,5446,5455,5472,5480,5483,5485,5492,5497,5502,5507,5509,5517,5528,5558,5697,5714,5749,5766,5785,5798,5799,5801,5817,5833,5834,5836,5849,5851,5852,5865,5869,5881,5884,5897,5900,5916,5932,5948,5963,5968,5978,5988,5992,5994,5997,6003,6008,6023,6026,6039,6053,6056,6067,6071,6082,6085,6098,6112,6126,6135,6140,6149,6154,6158,6161,6168,6174,6182,6187,6205,6209,6213,6317,6339,6342,6366,6381,6391,6489,6962,6966,6970,6975,6977,6982,6985,6987,6989,6991,6993,6995,6997,6999,7000,7004,7008,7013,7016,7021,7024,7027,7029,7032,7038,7043,7046,7049,7069,7072,7076,7081,7084,7089,7099,7209,7222,7231,7235,7247,7267,7269,7284,7389,7419,7423,7424,7426,7428,7431,7436,7444,7475,7549,7584,7665,7666,7831,7836,7853,7865,7885,7888,7912,7950,7972,7980,7995,8007,8015,8055,8078],
}

rad_platform_sensor_ObsError = {
#    'eos-2-airs': [0.1200000000E+01,0.1200000000E+01,0.1500000000E+01,0.1400000000E+01,0.1400000000E+01,0.1400000000E+01,0.1400000000E+01,0.1400000000E+01,1.250,1.250,1.200,1.200,1.200,1.200,1.200,1.200,1.150,1.150,1.150,1.150,1.150,1.150,1.150,1.150,1.150,1.150,1.150,1.150,1.125,1.050,1.050,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.950,1.100,0.950,0.950,1.000,1.100,1.100,1.100,1.100,1.100,1.100,1.100,1.100,0.950,1.100,0.950,1.000,1.100,1.400,0.950,0.850,0.900,0.900,0.900,0.800,0.800,0.850,0.800,0.950,0.900,0.850,1.000,1.150,1.000,0.850,0.900,1.200,1.000,0.900,0.900,0.900,1.000,0.900,0.900,0.900,0.900,0.900,1.400,0.850,0.2300000000E+01,0.900,0.900,0.900,0.900,0.900,0.850,0.850,0.900,0.900,0.900,0.900,0.900,0.900,0.900,0.900,0.900,0.900,1.150,0.900,0.900,0.900,0.900,0.900,0.900,0.950,0.950,0.950,0.950,0.950,0.900,0.925,0.900,0.900,0.900,0.900,0.850,0.800,0.750,0.750,0.750,0.850,0.900,0.900,0.900,0.900,0.900,0.900,1.000,1.000,1.000,1.000,0.850,0.950,0.950,0.950,0.900,0.800,0.850,0.750,0.750,0.750,0.800,0.750,0.800,0.900,0.750,0.800,0.800,0.1100000000E+01,0.750,0.1100000000E+01,0.750,0.800,0.700,0.850,1.100,0.850,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.600,0.650,0.600,0.550,0.500,0.525,0.550,0.500,0.500,0.550,0.555,0.575,0.550,0.650,0.700,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.1030000000E+05,0.600,0.700,0.650,0.675,0.700,0.750,0.775,0.800,0.800,0.850,0.850,0.850,0.700,0.700,0.700,0.700,0.700,0.700,0.700,0.725,0.750,0.775,0.800,0.825,0.800,0.800,0.800,0.750,0.800,0.800,0.800,0.800,0.800,0.850,0.800,0.800,0.1030000000E+05,0.750,0.750,0.750,0.750],
#    'fy3-1-mwhs': [0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2000000000E+01,0.2000000000E+01],
#    'fy3-1-mwts': [0.5000000000E+01,0.300,0.270,0.300],
#    'fy3-2-mwhs': [0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2000000000E+01,0.2000000000E+01],
#    'fy3-2-mwts': [0.5000000000E+01,0.300,0.270,0.300],
#    'fy3-3-mwhs2': [0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.1500000000E+01,0.1500000000E+01,0.1500000000E+01,0.1500000000E+01,0.1500000000E+01],
    'goes-16-abi': [2.720,1.790,1.920,1.740,5.000,wrfda_miss_float,3.080,3.060,2.820,1.740],
    'goes-17-abi': [wrfda_miss_float]*10,
    'himawari-8-ahi': [1.052,1.700,1.700,1.350,0.814,wrfda_miss_float,0.871,0.926,0.933,0.787],
#    'jpss-0-atms': [0.7000000000E+01,0.6000000000E+01,0.5000000000E+01,0.600,0.600,0.300,0.250,0.270,0.270,0.300,0.400,0.700,0.1100000000E+01,0.2100000000E+01,0.1000000000E+05,0.2500000000E+01,0.2500000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01,0.2000000000E+01],
#    'metop-1-amsua': [0.7000000000E+01,0.6000000000E+01,0.5000000000E+01,0.600,0.300,0.250,0.270,0.270,0.300,0.400,0.700,0.1100000000E+01,0.2100000000E+01,0.1000000000E+05,0.9000000000E+01],
#    'metop-1-iasi': [1.380,0.810,0.750,0.790,0.720,0.740,0.680,0.720,0.650,0.650,0.650,0.690,0.640,0.640,0.650,0.670,0.620,0.610,0.620,0.640,0.590,0.760,1.220,0.780,0.640,0.620,0.610,0.690,0.650,0.590,0.610,0.590,0.680,0.620,0.680,4.380,3.050,2.310,1.560,1.330,1.580,0.930,1.670,0.720,0.570,0.580,0.550,0.680,0.590,0.680,0.590,0.650,0.580,0.620,0.640,0.580,0.640,0.550,0.640,0.500,0.820,0.590,0.620,0.510,0.640,0.520,0.510,0.510,0.760,0.520,0.570,0.550,0.690,0.580,0.650,0.610,0.590,0.640,0.760,0.720,1.050,0.750,0.510,0.650,1.300,0.690,0.930,1.490,1.120,0.680,0.660,0.670,0.590,0.590,0.690,0.670,0.640,0.620,0.720,0.690,0.660,0.790,0.780,0.740,0.880,0.770,0.880,0.860,1.000,0.870,0.850,0.880,0.840,0.840,0.840,0.800,0.800,0.870,0.980,0.520,0.650,0.690,0.610,0.600,0.670,0.790,0.620,0.660,0.700,0.650,0.620,0.610,0.620,0.530,0.600,0.680,0.950,0.630,0.970,0.650,0.980,0.580,0.730,0.650,0.850,0.990,0.760,0.850,0.970,0.770,0.620,0.630,1.210,1.410,1.550,1.780,1.350,1.140,1.690,1.790,1.460,1.630,1.940,2.010,1.240,1.760,1.260,1.470,1.900,1.660,2.130,1.490,1.520,1.550,1.960,2.310,2.330,2.320,2.310,2.330,2.230,2.330,1.840,2.290,2.280,2.280,2.280,2.260,2.260,2.260,2.270,2.240,2.230,2.240,2.260,2.280,2.280,2.300,2.150,2.310,2.370,2.270,2.290,2.290,2.230,2.280,2.320,2.320,2.310,2.320,2.320,2.310,2.310,2.280,2.290,2.280,2.260,2.290,2.270,2.260,2.250,2.270,2.240,2.210,2.240,2.170,2.180,2.170,2.210,1.990,2.160,2.200,2.130,2.120,2.130,2.100,2.120,2.110,2.090,2.090,2.080,2.090,2.040,2.040,2.100,2.010,2.050,2.030,2.060,1.980,1.950,1.940,1.910,1.700,1.760,1.770,1.830,2.040,1.910,1.990,1.990,2.070,2.020,2.040,2.100,2.060,2.180,2.210,2.240,2.230,2.230,1.980,2.200,2.180,2.180,2.210,2.230,2.240,2.240,2.250,1.800,2.240,1.730,1.730,2.270,1.670,2.210,1.720,2.230,2.230,2.230,2.240,2.230,2.120,2.170,1.740,2.020,1.880,1.670,1.730,1.830,1.820,1.730,1.830,2.190,1.840,1.890,1.600,1.710,1.860,1.850,1.840,1.870,1.910,1.520,1.950,1.870,1.890,1.910,1.910,1.930,1.900,1.910,1.900,1.890,1.890,1.910,1.900,1.910,1.910,1.910,1.930,1.940,1.910,1.920,1.770,1.910,1.950,1.190,1.960,1.980,1.940,1.550,1.910,1.920,1.920,1.970,1.930,1.990,1.860,1.120,1.930,1.920,1.950,1.850,1.840,1.910,1.120,1.820,1.820,1.950,1.240,1.940,1.960,1.210,1.830,1.960,1.360,1.960,1.820,1.920,1.680,1.930,1.230,1.960,1.930,1.860,1.410,1.160,1.600,1.250,1.200,1.650,1.660,1.870,1.940,1.960,1.910,1.250,1.930,1.910,1.700,0.990,1.810,1.920,1.950,1.500,1.470,1.150,1.580,1.180,1.820,1.130,1.830,1.910,1.260,1.270,1.910,1.450,1.600,1.290,1.940,1.940,1.230,1.950,1.210,1.940,1.860,1.900,1.330,1.750,2.020,1.980,2.030,1.830,1.500,2.040,2.020,1.900,2.000,2.020,1.950,1.930,1.950,1.950,1.990,2.000,1.940,1.960,1.860,1.920,1.880,1.860,1.840,1.870,1.770,1.890,1.890,1.880,1.940,1.820,1.790,1.860,2.060,2.330,1.880,1.860,1.810,1.800,1.800,1.860,1.900,2.000,2.060,2.100,2.200,2.000,2.160,1.980,1.800,1.800,1.850,1.750,2.040,2.190,2.140,2.190,1.860,2.100,2.110,2.180,2.030,2.280,2.190,2.260,2.260,2.210,2.210,2.260,2.330,2.270,2.210,2.120,2.230,2.260,2.250,1.880,2.260,2.240,2.360,2.290,2.350,2.300,2.270,2.080,2.050,2.270,2.280,2.270,2.280,1.970,2.250,2.250,2.250,2.310,2.280,2.270,2.130,2.240,2.280,2.280,2.410,2.340,9.320,2.280,2.380,2.270,2.270,2.390,2.110,2.090,2.100,2.060,2.120,2.080,2.000,1.930,2.020,2.550,1.540,1.640,1.510,1.550,2.820,2.920,2.550,2.370,1.850,1.600,1.720,1.740,1.790,1.900,1.940,2.000,2.040,2.080,2.120,2.130,2.160,2.180,2.180,2.200,2.200,2.410,2.390,2.380,2.400,2.420,2.410,2.430,2.450,2.430,2.450,2.430,2.400,2.440,2.400,2.420,2.430,2.450,2.450,2.450,2.460,2.450,2.450,2.430,2.510,2.480,2.480,2.530,2.460,2.490,2.500,2.500,2.500,2.520,2.520,2.540,2.500,2.480,2.500,2.550,2.500,2.480,2.500,2.500,2.520,2.520,2.480,2.500,2.500,2.520,2.460,2.530,9.000],
#    'metop-1-mhs': [0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2000000000E+01,0.2000000000E+01],
#    'metop-2-amsua': [0.7000000000E+01,0.6000000000E+01,0.5000000000E+01,0.600,0.300,0.250,0.270,0.270,0.300,0.400,0.700,0.1100000000E+01,0.2100000000E+01,0.1000000000E+05,0.9000000000E+01],
#    'metop-2-iasi': [1.380,0.810,0.750,0.790,0.720,0.740,0.680,0.720,0.650,0.650,0.650,0.690,0.640,0.640,0.650,0.670,0.620,0.610,0.620,0.640,0.590,0.760,1.220,0.780,0.640,0.620,0.610,0.690,0.650,0.590,0.610,0.590,0.680,0.620,0.680,4.380,3.050,2.310,1.560,1.330,1.580,0.930,1.670,0.720,0.570,0.580,0.550,0.680,0.590,0.680,0.590,0.650,0.580,0.620,0.640,0.580,0.640,0.550,0.640,0.500,0.820,0.590,0.620,0.510,0.640,0.520,0.510,0.510,0.760,0.520,0.570,0.550,0.690,0.580,0.650,0.610,0.590,0.640,0.760,0.720,1.050,0.750,0.510,0.650,1.300,0.690,0.930,1.490,1.120,0.680,0.660,0.670,0.590,0.590,0.690,0.670,0.640,0.620,0.720,0.690,0.660,0.790,0.780,0.740,0.880,0.770,0.880,0.860,1.000,0.870,0.850,0.880,0.840,0.840,0.840,0.800,0.800,0.870,0.980,0.520,0.650,0.690,0.610,0.600,0.670,0.790,0.620,0.660,0.700,0.650,0.620,0.610,0.620,0.530,0.600,0.680,0.950,0.630,0.970,0.650,0.980,0.580,0.730,0.650,0.850,0.990,0.760,0.850,0.970,0.770,0.620,0.630,1.210,1.410,1.550,1.780,1.350,1.140,1.690,1.790,1.460,1.630,1.940,2.010,1.240,1.760,1.260,1.470,1.900,1.660,2.130,1.490,1.520,1.550,1.960,2.310,2.330,2.320,2.310,2.330,2.230,2.330,1.840,2.290,2.280,2.280,2.280,2.260,2.260,2.260,2.270,2.240,2.230,2.240,2.260,2.280,2.280,2.300,2.150,2.310,2.370,2.270,2.290,2.290,2.230,2.280,2.320,2.320,2.310,2.320,2.320,2.310,2.310,2.280,2.290,2.280,2.260,2.290,2.270,2.260,2.250,2.270,2.240,2.210,2.240,2.170,2.180,2.170,2.210,1.990,2.160,2.200,2.130,2.120,2.130,2.100,2.120,2.110,2.090,2.090,2.080,2.090,2.040,2.040,2.100,2.010,2.050,2.030,2.060,1.980,1.950,1.940,1.910,1.700,1.760,1.770,1.830,2.040,1.910,1.990,1.990,2.070,2.020,2.040,2.100,2.060,2.180,2.210,2.240,2.230,2.230,1.980,2.200,2.180,2.180,2.210,2.230,2.240,2.240,2.250,1.800,2.240,1.730,1.730,2.270,1.670,2.210,1.720,2.230,2.230,2.230,2.240,2.230,2.120,2.170,1.740,2.020,1.880,1.670,1.730,1.830,1.820,1.730,1.830,2.190,1.840,1.890,1.600,1.710,1.860,1.850,1.840,1.870,1.910,1.520,1.950,1.870,1.890,1.910,1.910,1.930,1.900,1.910,1.900,1.890,1.890,1.910,1.900,1.910,1.910,1.910,1.930,1.940,1.910,1.920,1.770,1.910,1.950,1.190,1.960,1.980,1.940,1.550,1.910,1.920,1.920,1.970,1.930,1.990,1.860,1.120,1.930,1.920,1.950,1.850,1.840,1.910,1.120,1.820,1.820,1.950,1.240,1.940,1.960,1.210,1.830,1.960,1.360,1.960,1.820,1.920,1.680,1.930,1.230,1.960,1.930,1.860,1.410,1.160,1.600,1.250,1.200,1.650,1.660,1.870,1.940,1.960,1.910,1.250,1.930,1.910,1.700,0.990,1.810,1.920,1.950,1.500,1.470,1.150,1.580,1.180,1.820,1.130,1.830,1.910,1.260,1.270,1.910,1.450,1.600,1.290,1.940,1.940,1.230,1.950,1.210,1.940,1.860,1.900,1.330,1.750,2.020,1.980,2.030,1.830,1.500,2.040,2.020,1.900,2.000,2.020,1.950,1.930,1.950,1.950,1.990,2.000,1.940,1.960,1.860,1.920,1.880,1.860,1.840,1.870,1.770,1.890,1.890,1.880,1.940,1.820,1.790,1.860,2.060,2.330,1.880,1.860,1.810,1.800,1.800,1.860,1.900,2.000,2.060,2.100,2.200,2.000,2.160,1.980,1.800,1.800,1.850,1.750,2.040,2.190,2.140,2.190,1.860,2.100,2.110,2.180,2.030,2.280,2.190,2.260,2.260,2.210,2.210,2.260,2.330,2.270,2.210,2.120,2.230,2.260,2.250,1.880,2.260,2.240,2.360,2.290,2.350,2.300,2.270,2.080,2.050,2.270,2.280,2.270,2.280,1.970,2.250,2.250,2.250,2.310,2.280,2.270,2.130,2.240,2.280,2.280,2.410,2.340,9.320,2.280,2.380,2.270,2.270,2.390,2.110,2.090,2.100,2.060,2.120,2.080,2.000,1.930,2.020,2.550,1.540,1.640,1.510,1.550,2.820,2.920,2.550,2.370,1.850,1.600,1.720,1.740,1.790,1.900,1.940,2.000,2.040,2.080,2.120,2.130,2.160,2.180,2.180,2.200,2.200,2.410,2.390,2.380,2.400,2.420,2.410,2.430,2.450,2.430,2.450,2.430,2.400,2.440,2.400,2.420,2.430,2.450,2.450,2.450,2.460,2.450,2.450,2.430,2.510,2.480,2.480,2.530,2.460,2.490,2.500,2.500,2.500,2.520,2.520,2.540,2.500,2.480,2.500,2.550,2.500,2.480,2.500,2.500,2.520,2.520,2.480,2.500,2.500,2.520,2.460,2.530,9.000],
#    'metop-2-mhs': [0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2000000000E+01,0.2000000000E+01],
#    'msg-2-seviri': [1.800,2.500,2.250,1.250,1.250,1.250,1.450,1.250],
#    'msg-3-seviri': [1.800,2.500,2.250,1.250,1.250,1.250,1.450,1.250],
#    'noaa-15-amsua': [0.7000000000E+01,0.6000000000E+01,0.5000000000E+01,0.600,0.300,0.230,0.250,0.275,0.340,0.400,0.3000000000E+01,0.1000000000E+01,0.1500000000E+01,0.1000000000E+01,0.7000000000E+01],
#    'noaa-16-amsua': [0.7000000000E+01,0.6000000000E+01,0.5000000000E+01,0.550,0.300,0.250,0.235,0.400,0.300,0.400,0.600,0.1000000000E+01,0.1500000000E+01,0.1000000000E+01,0.7000000000E+01],
#    'noaa-16-amsub': [0.6000000000E+01,0.3750000000E+01,0.3500000000E+01,0.3000000000E+01,0.2800000000E+01,0.1000000000E+05,0.700,0.570,0.420,0.355,0.460,0.530,0.1000000000E+01,0.1100000000E+01,0.550,0.1100000000E+01,0.1700000000E+01,0.450,0.250,0.300,0.1000000000E+05,0.1000000000E+05,0.1000000000E+05,0.1000000000E+05],
#    'noaa-17-hirs': [0.1000000000E+05,0.600,0.530,0.400,0.360,0.460,0.570,0.1000000000E+01,0.1100000000E+01,0.600,0.1200000000E+01,0.1600000000E+01,0.364,0.260,0.260,0.1000000000E+05,0.1000000000E+05,0.1000000000E+05,0.1000000000E+05],
#    'noaa-18-amsua': [0.7000000000E+01,0.6000000000E+01,0.5000000000E+01,0.600,0.300,0.250,0.270,0.270,0.300,0.400,0.700,0.1100000000E+01,0.2100000000E+01,0.1000000000E+05,0.9000000000E+01],
#    'noaa-18-hirs': [0.1000000000E+05,0.600,0.530,0.400,0.360,0.460,0.570,0.1000000000E+01,0.1100000000E+01,0.600,0.1200000000E+01,0.1600000000E+01,0.364,0.260,0.260,0.1000000000E+05,0.1000000000E+05,0.1000000000E+05,0.1000000000E+05],
#    'noaa-18-mhs': [0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2000000000E+01,0.2000000000E+01],
#    'noaa-19-amsua': [0.7000000000E+01,0.6000000000E+01,0.5000000000E+01,0.600,0.300,0.250,0.270,0.270,0.300,0.400,0.700,0.1100000000E+01,0.2100000000E+01,0.1000000000E+05,0.9000000000E+01],
#    'noaa-19-mhs': [0.2500000000E+01,0.2500000000E+01,0.2500000000E+01,0.2000000000E+01,0.2000000000E+01],
}
#Note: ABI/AHI channel 12 is sensitive to O3, which is not included in WRFDA RTM interfaces
#      Therefore std is not relevant

# units (exact copy from gsi_ncdiag.py)
# 'IODA/UFO_variable_name': 'Unit'
units_values = {
    'virtual_temperature': 'K',
    'atmosphere_ln_pressure_coordinate': '1',
    'specific_humidity': '1',
    'northward_wind': 'm s-1',
    'eastward_wind': 'm s-1',
    'geopotential_height': 'm',
    'height_above_mean_sea_level': 'm',
    'surface_pressure': 'Pa',
    'surface_temperature': 'K',
    'surface_roughness_length': 'm',
    'surface_geopotential_height': 'm',
    'land_area_fraction': '1',
    'air_temperature': 'K',
    'air_pressure': 'Pa',
    'air_pressure_levels': 'Pa',
    'humidity_mixing_ratio': '1',
    'mole_fraction_of_carbon_dioxide_in_air': '1',
    'mole_fraction_of_ozone_in_air': '1',
    'atmosphere_mass_content_of_cloud_liquid_water': 'kg m-2',
    'effective_radius_of_cloud_liquid_water_particle': 'm',
    'atmosphere_mass_content_of_cloud_ice': 'kg m-2',
    'effective_radius_of_cloud_ice_particle': 'm',
    'water_area_fraction': '1',
    'land_area_fraction': '1',
    'ice_area_fraction': '1',
    'surface_snow_area_fraction': '1',
    'vegetation_area_fraction': '1',
    'surface_temperature_where_sea': 'K',
    'surface_temperature_where_land': 'K',
    'surface_temperature_where_ice': 'K',
    'surface_temperature_where_snow': 'K',
    'surface_wind_speed': 'm s-1',
    'surface_wind_from_direction': 'degree',
    'leaf_area_index': '1',
    'volume_fraction_of_condensed_water_in_soil': '1',
    'soil_temperature': 'K',
    'land_type_index': '1',
    'vegetation_type_index': '1',
    'soil_type': '1',
    'surface_snow_thickness': 'm',
    'humidity_mixing_ratio': '1',
    'wind_reduction_factor_at_10m': '1',
    'sulf': '1',
    'bc1': '1',
    'bc2': '1',
    'oc1': '1',
    'oc2': '1',
    'dust1': '1',
    'dust2': '1',
    'dust3': '1',
    'dust4': '1',
    'dust5': '1',
    'seas1': '1',
    'seas2': '1',
    'seas3': '1',
    'seas4': '1',
    'latitude': 'degrees_north',
    'longitude': 'degrees_east',
    'station_elevation': 'm',
    'height': 'm',
    'height_above_mean_sea_level': 'm',
    'cloud_area_fraction': '1',
    'scan_position': '1',
    'sensor_azimuth_angle': 'degree',
    'sensor_zenith_angle': 'degree',
    'sensor_view_angle': 'degree',
    'solar_zenith_angle': 'degree',
    'solar_azimuth_angle': 'degree',
    'modis_deep_blue_flag': '1',
    'row_anomaly_index': '1',
    'top_level_pressure': 'Pa',
    'bottom_level_pressure': 'Pa',
    'tropopause_pressure': 'Pa',
    'brightness_temperature_jacobian_surface_temperature': '1',
    'brightness_temperature_jacobian_surface_emissivity': 'K',
    'brightness_temperature_jacobian_air_temperature': '1',
    'brightness_temperature_jacobian_humidity_mixing_ratio': 'K/g/Kg ',
    'optical_thickness_of_atmosphere_layer': '1',
}

# @TestReference
# fields from WRFDA to compare to computations done in UFO
test_fields = {
}

###############################################################################
###############################################################################

# satellite radiance observations
class Radiances:
    """ class Radiances - satellite radiance observations

                Use this class to read in satellite radiance observations
                from WRFDA netCDF diag files

    Functions:

    Attributes:
      filename    - string path to file
      validtime   - datetime object of valid observation time
      nobs        - number of observations


  """

    def __init__(self, filename):
        self.filename = filename
        splitfname = self.filename.split('/')[-1].split('_')
        i = False
        for s in rad_platform_sensor_combos:
            if s in splitfname:
                self.platform_sensor = s
                i = splitfname.index(s)
#                self.obstype = "_".join(splitfname[i:i + 2])
        if not i:
            raise ValueError("Observation is not a radiance type...")

    def read(self):
        import netCDF4 as nc
        import datetime as dt
        # get valid time
        df = nc.Dataset(self.filename)
        tstr = self.filename.split('/')[-1].split('_')[-1].split('.')[0]
        self.validtime = dt.datetime.strptime(tstr, "%Y%m%d%H")
        # sensor and satellite
        self.sensor = self.platform_sensor.split('-')[-1]
        self.satellite = "-".join(self.platform_sensor.split('-')[0:-1])

        # number of observations
        self.nlocs = len(df.dimensions['npixel'])
        self.nchans = len(df.dimensions['nchan'])
        self.nobs = self.nlocs * self.nchans
        self.df = df

    def close(self):
        self.df.close()

    def toIODAobs(self, OutDir, clobber=True):
        """ toIODAobs(OutDir,clobber=True)
     output observations from the specified WRFDA diag file
     to the JEDI/IODA observation format
        """
        import ioda_conv_ncio as iconv
        import os
        import errno
        from collections import defaultdict, OrderedDict
        from orddicts import DefaultOrderedDict
        import numpy as np
        import datetime as dt
        import netCDF4 as nc

        # place files for individual dates in separate directories
        fullOutDir = OutDir + '/' + self.validtime.strftime("%Y%m%d%H")
        try:
            os.makedirs(fullOutDir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(fullOutDir):
                pass

        # set up a NcWriter class
        outname = fullOutDir + '/' + self.sensor + '_' + self.satellite + \
            '_obs_' + self.validtime.strftime("%Y%m%d%H") + '.nc4'
        if not clobber:
            if (os.path.exists(outname)):
                print("File exists. Skipping and not overwriting:")
                print(outname)
                return
        RecKeyList = []
        LocKeyList = []
        TestKeyList = []
        LocVars = []
        TestVars = []
        AttrData = {}
        varDict = defaultdict(lambda: defaultdict(dict))
        outdata = defaultdict(lambda: DefaultOrderedDict(OrderedDict))
        rec_mdata = defaultdict(lambda: DefaultOrderedDict(OrderedDict))
        loc_mdata = defaultdict(lambda: DefaultOrderedDict(OrderedDict))
        var_mdata = defaultdict(lambda: DefaultOrderedDict(OrderedDict))
        test_mdata = defaultdict(lambda: DefaultOrderedDict(OrderedDict))
        # get list of location variable for this var/platform
        for ncv in self.df.variables:
            if ncv in all_LocKeyList:
                for val in all_LocKeyList[ncv]:
                    LocKeyList.append(val)
                    LocVars.append(ncv)

        # get list of TestReference variables for this var/platform
        for ncv in self.df.variables:
            if ncv in test_fields:
                TestKeyList.append(test_fields[ncv])
                TestVars.append(ncv)

        # for now, record len is 1 and the list is empty?
        recKey = 0
        writer = iconv.NcWriter(outname, RecKeyList, LocKeyList, TestKeyList=TestKeyList)

        if self.sensor in sensor_chanlist_dict:
            chanlist = sensor_chanlist_dict[self.sensor]
        else:
            chanlist = list(range(1,self.nchan+1))
        nchans = len(chanlist)

        for chan in chanlist:
            value = "brightness_temperature_{:d}".format(chan)
            varDict[value]['valKey'] = value, writer.OvalName()
            varDict[value]['errKey'] = value, writer.OerrName()
            varDict[value]['qcKey'] = value, writer.OqcName()
            units_values[value] = 'K'

        for ivar, lvar in enumerate(LocVars):
            loc_mdata_name = LocKeyList[ivar][0]
            loc_mdata_type = LocKeyList[ivar][1]
            if lvar == 'date':
                tmp = self.df[lvar][:]
                obstimes = [dt.datetime.strptime("".join(a.astype(str)), "%Y-%m-%d_%H:%M:%S") for a in tmp]
                obstimes = [a.strftime("%Y-%m-%dT%H:%M:%SZ") for a in obstimes]
                loc_mdata[loc_mdata_name] = writer.FillNcVector(obstimes, "datetime")
            else:
                if loc_mdata_type == 'float':
                    tmp = self.df[lvar][:].astype(float)
                    tmp[tmp <= wrfda_miss_float] = nc.default_fillvals['f4']
                else:
                    tmp = self.df[lvar][:]
                loc_mdata[loc_mdata_name] = tmp

        # put the TestReference fields in the structure for writing out
        for tvar in TestVars:
            test_mdata_name = test_fields[tvar][0]
            tmp = self.df[tvar][:]
            tmp[tmp <= wrfda_miss_float] = nc.default_fillvals['f4']
            test_mdata[test_mdata_name] = tmp

        # check for additional WRFDA output for each variable
        for wrfdavar, iodavar in wrfda_add_vars.items():
            if wrfdavar in self.df.variables:
                tmp = np.transpose(np.asarray(self.df[wrfdavar]))

                tmp[tmp <= wrfda_miss_float] = nc.default_fillvals['f4']
                for c, chan in enumerate(chanlist):
                    varname = "brightness_temperature_{:d}".format(chan)
                    gvname = varname, iodavar
                    outvals = tmp[c]
                    outdata[gvname] = outvals

        # tb_obs, tb_err, and tb_qc are nlocs x nchan
        # --> using transpose speeds up access below
        obsdata = np.transpose(np.asarray(self.df['tb_obs']))
        obserr = rad_platform_sensor_ObsError[self.platform_sensor]
        # obserr  = np.transpose(np.asarray(self.df['tb_err']))
        obsqc   = np.transpose(np.asarray(self.df['tb_qc']))

        # loop through channels for subset
        var_names = []
        for c, chan in enumerate(chanlist):
            value = "brightness_temperature_{:d}".format(chan)
            var_names.append(value)

            obsdatasub = obsdata[c]
            obsdatasub[obsdatasub <= wrfda_miss_float] = nc.default_fillvals['f4']

            obserrsub = np.full(self.nlocs, obserr[c])
            obserrsub[obserrsub <= wrfda_miss_float] = nc.default_fillvals['f4']

            obsqcsub = obsqc[c]
            obsqcsub[obsqcsub <= wrfda_miss_int] = nc.default_fillvals['i4']

            # store values in output data dictionary
            outdata[varDict[value]['valKey']] = obsdatasub
            outdata[varDict[value]['errKey']] = obserrsub
            outdata[varDict[value]['qcKey']] = obsqcsub.astype(int)

        # var metadata
        var_mdata['variable_names'] = writer.FillNcVector(var_names, "string")
        var_mdata['sensor_channel'] = np.asarray(chanlist)

        # dummy record metadata, for now
        nrecs = 1
        rec_mdata['rec_id'] = np.asarray([999], dtype='i4')
        loc_mdata['record_number'] = np.full((self.nlocs), 1, dtype='i4')

        # global attributes

        AttrData["date_time_string"] = self.validtime.strftime("%Y-%m-%dT%H:%M:%SZ")
        AttrData["satellite"] = self.satellite
        AttrData["sensor"] = self.sensor

        # set dimension lengths in the writer since we are bypassing
        # ExtractObsData
        writer._nrecs = nrecs
        writer._nvars = nchans
        writer._nlocs = self.nlocs

        writer.BuildNetcdf(outdata, rec_mdata, loc_mdata, var_mdata,
                           AttrData, units_values, test_mdata)
        print("Satellite radiance obs processed, wrote to:")
        print(outname)

