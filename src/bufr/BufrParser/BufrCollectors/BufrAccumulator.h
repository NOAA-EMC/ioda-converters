/*
 * (C) Copyright 2020 NOAA/NWS/NCEP/EMC
 *
 * This software is licensed under the terms of the Apache Licence Version 2.0
 * which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
 */

#pragma once

#include <gsl/gsl>
#include <set>

#include "Eigen/Dense"

#include "BufrParser/BufrTypes.h"

namespace Ingester
{
    class BufrAccumulator
    {
     public:
        explicit BufrAccumulator(Eigen::Index numColumns, Eigen::Index blockSize = 50000);

        void addRow(std::vector<double> newRow);
        IngesterArray getData(Eigen::Index startCol, const Channels& channels);
        void reset();

        //Getters
        inline Eigen::Index getNumColumns() const { return numColumns_; }

     private:
        IngesterArray dataArray_;
        Eigen::Index numColumns_;
        Eigen::Index numDataRows_;
        Eigen::Index blockSize_;
    };
}  // namespace Ingester
