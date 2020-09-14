//
// Created by Ronald McLaren on 9/2/20.
//

#pragma once

#include <string>
#include <vector>


#include "eckit/config/LocalConfiguration.h"

#include "BufrParser/BufrTypes.h"
#include "DataObject/StrVecDataObject.h"
#include "Export.h"


namespace Ingester
{
    class DatetimeExport : public Export
    {
     public:
        explicit DatetimeExport(const eckit::Configuration& conf);
        ~DatetimeExport() override = default;

        std::shared_ptr<DataObject> exportData(BufrDataMap map);

     private:
        const std::string yearKey_;
        const std::string monthKey_;
        const std::string dayKey_;
        const std::string hourKey_;
        const std::string minuteKey_;
        const std::string secondKey_;
        const bool isUTC_;
    };
}  // namespace Ingester
