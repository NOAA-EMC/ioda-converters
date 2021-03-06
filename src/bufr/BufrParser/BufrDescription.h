/*
 * (C) Copyright 2020 NOAA/NWS/NCEP/EMC
 *
 * This software is licensed under the terms of the Apache Licence Version 2.0
 * which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
 */

#pragma once

#include <map>
#include <string>
#include <vector>

#include "eckit/config/LocalConfiguration.h"

#include "BufrTypes.h"


namespace Ingester
{
    class BufrMnemonicSet;
    class Export;

    /// \brief Description of the data to be read from a BUFR file and how to expose that data to
    /// the outside world.
    class BufrDescription
    {
     public:
        BufrDescription() = default;
        explicit BufrDescription(const eckit::Configuration& conf);

        /// \brief Add a BufrMnemonicSet to the description.
        /// \param mnemonicSet BufrMnemonicSet to add
        void addMnemonicSet(const BufrMnemonicSet& mnemonicSet);

        /// \brief Add an Export description.
        /// \param key string that defines the name of the export
        /// \param bufrExport Export shared ptr to an Export instance
        void addExport(const std::string& key, const std::shared_ptr<Export>& bufrExport);

        // Setters
        inline void setFilepath(const std::string& filepath) { filepath_ = filepath; }

        // Getters
        inline std::vector<BufrMnemonicSet> getMnemonicSets() const { return mnemonicSets_; }
        inline std::string filepath() const { return filepath_; }
        inline ExportMap getExportMap() const { return exportMap_; }

     private:
        /// \brief Sets of mnemonic strings for the data to read.
        std::vector<BufrMnemonicSet> mnemonicSets_;

        /// \brief Specifies the relative path to the BUFR file to read.
        std::string filepath_;

        /// \brief Map of export strings to Export classes.
        ExportMap exportMap_;
    };
}  // namespace Ingester
