"""
Copyright (c) 2016, Battelle Memorial Institute
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies,
either expressed or implied, of the FreeBSD Project.


This material was prepared as an account of work sponsored by an
agency of the United States Government.  Neither the United States
Government nor the United States Department of Energy, nor Battelle,
nor any of their employees, nor any jurisdiction or organization
that has cooperated in the development of these materials, makes
any warranty, express or implied, or assumes any legal liability
or responsibility for the accuracy, completeness, or usefulness or
any information, apparatus, product, software, or process disclosed,
or represents that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or
service by trade name, trademark, manufacturer, or otherwise does
not necessarily constitute or imply its endorsement, recommendation,
r favoring by the United States Government or any agency thereof,
or Battelle Memorial Institute. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the
United States Government or any agency thereof.

PACIFIC NORTHWEST NATIONAL LABORATORY
operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
under Contract DE-AC05-76RL01830
"""
import datetime
from datetime import datetime
from dateutil.parser import parse
from .common import create_table_key, pre_conditions, check_run_status
from volttron.platform.agent.math_utils import mean
import logging

_log = logging.getLogger(__name__)

DUCT_STC_RCX3 = "No Static Pressure Reset Dx"
SA_TEMP_RCX3 = "No Supply-air Temperature Reset Dx"
SCHED_RCX = "Operational Schedule Dx"
DX = "/diagnostic message"

INCONSISTENT_DATE = -89.2
INSUFFICIENT_DATA = -79.2


class SchedResetAIRCx(object):
    """
    Operational schedule, supply-air temperature set point reset, and duct static pressure reset
    AIRCx for AHUs or RTUs.
    """
    def __init__(self, unocc_time_thr, unocc_stcpr_thr,
                 monday_sch, tuesday_sch, wednesday_sch, thursday_sch,
                 friday_sch, saturday_sch, sunday_sch,
                 no_req_data, stcpr_reset_thr, sat_reset_thr,
                 analysis):
        self.fan_status_array = []
        self.schedule = {}
        self.stcpr_array = []
        self.schedule_time_array = []

        self.stcpr_stpt_array = []
        self.sat_stpt_array = []
        self.reset_table_key = None
        self.timestamp_array = []
        self.dx_table = {}

        def date_parse(dates):
            return [parse(timestamp_array).time() for timestamp_array in dates]

        self.analysis = analysis
        self.monday_sch = date_parse(monday_sch)
        self.tuesday_sch = date_parse(tuesday_sch)
        self.wednesday_sch = date_parse(wednesday_sch)
        self.thursday_sch = date_parse(thursday_sch)
        self.friday_sch = date_parse(friday_sch)
        self.saturday_sch = date_parse(saturday_sch)
        self.sunday_sch = date_parse(sunday_sch)

        self.schedule = {0: self.monday_sch, 1: self.tuesday_sch,
                         2: self.wednesday_sch, 3: self.thursday_sch,
                         4: self.friday_sch, 5: self.saturday_sch,
                         6: self.sunday_sch}
        self.pre_msg = ("Current time is in the scheduled hours "
                        "unit is operating correctly.")

        # Application thresholds (Configurable)
        self.no_req_data = no_req_data
        self.unocc_time_thr = unocc_time_thr
        self.unocc_stcpr_thr = unocc_stcpr_thr
        self.stcpr_reset_thr = stcpr_reset_thr
        self.sat_reset_thr = sat_reset_thr

    def reinitialize_sched(self):
        """
        Reinitialize schedule data arrays
        :return:
        """
        self.stcpr_array = []
        self.fan_status_array = []
        self.schedule_time_array = []

    def schedule_reset_aircx(self, current_time, stcpr_data, stcpr_stpt_data,
                             sat_stpt_data, current_fan_status, dx_result):
        """
        Calls Schedule AIRCx and Set Point Reset AIRCx.
        :param current_time:
        :param stcpr_data:
        :param stcpr_stpt_data:
        :param sat_stpt_data:
        :param current_fan_status:
        :param dx_result:
        :return:
        """

        dx_result = self.sched_aircx(current_time, stcpr_data, current_fan_status, dx_result)
        dx_result = self.setpoint_reset_aircx(current_time, current_fan_status,
                                              stcpr_stpt_data, sat_stpt_data, dx_result)
        self.timestamp_array.append(current_time)
        return dx_result

    def sched_aircx(self, current_time, stcpr_data, current_fan_status, dx_result):
        """
        Main function for operation schedule AIRCx - manages data arrays checks AIRCx run status.
        :param current_time:
        :param stcpr_data:
        :param current_fan_status:
        :param dx_result:
        :return:
        """
        schedule = self.schedule[current_time.weekday()]
        run_status = check_run_status(self.timestamp_array, current_time, self.no_req_data, run_schedule="daily")
        _log.debug("sched_aricx ::: schdule: {}".format(schedule))
        _log.debug("sched_aricx ::: run_status: {}".format(run_status))
        if run_status is None:
            schedule_name = create_table_key(self.analysis, self.timestamp_array[0])
            dx_result.log("{} - Insufficient data to produce a valid diagnostic result.".format(current_time))
            dx_result = pre_conditions(INSUFFICIENT_DATA, [SCHED_RCX], schedule_name, current_time, dx_result)
            self.reinitialize_sched()

        if run_status:
            _log.debug("sched_aricx ::: unocc_fan_operation Entrance")
            dx_result = self.unocc_fan_operation(dx_result)
            self.reinitialize_sched()

        if current_time.time() < schedule[0] or current_time.time() > schedule[1]:
            self.stcpr_array.extend(stcpr_data)
            self.fan_status_array.append((current_time, current_fan_status))
            self.schedule_time_array.append(current_time)
        return dx_result


    def setpoint_reset_aircx(self, current_time, current_fan_status, stcpr_stpt_data, sat_stpt_data, dx_result):
        """
        Main function for set point reset AIRCx - manages data arrays checks AIRCx run status.
        :param current_time:
        :param current_fan_status:
        :param stcpr_stpt_data:
        :param sat_stpt_data:
        :param dx_result:
        :return:
        """
        stcpr_run_status = check_run_status(self.timestamp_array, current_time, self.no_req_data,
                                            run_schedule="daily", minimum_point_array=self.stcpr_stpt_array)
        # _log.debug("setpoint_reset_aircx ::: stcpr_run_status: {}".format(stcpr_run_status))
        if not self.timestamp_array:
            return dx_result

        self.reset_table_key = reset_name = create_table_key(self.analysis, self.timestamp_array[0])
        if stcpr_run_status is None:
            dx_result.log("{} - Insufficient data to produce - {}".format(current_time, DUCT_STC_RCX3))
            dx_result = pre_conditions(INSUFFICIENT_DATA, [DUCT_STC_RCX3], reset_name, current_time, dx_result)
            self.stcpr_stpt_array = []
        elif stcpr_run_status:
            # _log.debug("setpoint_reset_aircx ::: no_static_pr_reset Entrance")
            dx_result = self.no_static_pr_reset(dx_result)
            self.stcpr_stpt_array = []

        sat_run_status = check_run_status(self.timestamp_array, current_time, self.no_req_data,
                                          run_schedule="daily", minimum_point_array=self.sat_stpt_array)
        # _log.debug("setpoint_reset_aircx ::: sat_run_status: {}".format(sat_run_status))
        if sat_run_status is None:
            dx_result.log("{} - Insufficient data to produce - {}".format(current_time, SA_TEMP_RCX3))
            dx_result = pre_conditions(INSUFFICIENT_DATA, [SA_TEMP_RCX3], reset_name, current_time, dx_result)
            self.sat_stpt_array = []
            self.timestamp_array = []
        elif sat_run_status:
            # _log.debug("setpoint_reset_aircx ::: no_sat_stpt_reset Entrance")
            dx_result = self.no_sat_stpt_reset(dx_result)
            self.sat_stpt_array = []
            self.timestamp_array = []

        if current_fan_status:
            if stcpr_stpt_data:
                self.stcpr_stpt_array.append(mean(stcpr_stpt_data))
            if sat_stpt_data:
                self.sat_stpt_array.append(mean(sat_stpt_data))

        return dx_result

    def unocc_fan_operation(self, dx_result):
        """
        AIRCx to determine if AHU is operating excessively in unoccupied mode.
        :param dx_result:
        :return:
        """
        # _log.debug("unocc_fan_operation ::: unocc_fan_operation Entrance success:::")
        avg_duct_stcpr = 0
        percent_on = 0
        fan_status_on = [(fan[0].hour, fan[1]) for fan in self.fan_status_array if int(fan[1]) == 1]
        fanstat = [(fan[0].hour, fan[1]) for fan in self.fan_status_array]
        hourly_counter = []
        thresholds = zip(self.unocc_time_thr.items(), self.unocc_stcpr_thr.items())
        # _log.debug("unocc_fan_operation ::: thresholds: {}".format(thresholds))
        diagnostic_msg = {}

        for counter in range(24):
            fan_on_count = [fan_status_time[1] for fan_status_time in fan_status_on if fan_status_time[0] == counter]
            fan_count = [fan_status_time[1] for fan_status_time in fanstat if fan_status_time[0] == counter]
            if len(fan_count):
                hourly_counter.append(fan_on_count.count(1)/len(fan_count)*100)
            else:
                hourly_counter.append(0)
        # _log.debug("unocc_fan_operation ::: hourly_counter: {}".format(hourly_counter))
        if self.schedule_time_array:
            if self.fan_status_array:
                percent_on = (len(fan_status_on)/len(self.fan_status_array)) * 100.0
                # _log.debug("unocc_fan_operation ::: fan_status_on: {}".format(fan_status_on))
                # _log.debug("unocc_fan_operation ::: fan_status_array: {}".format(self.fan_status_array))
                # _log.debug("unocc_fan_operation ::: percent_on: {}".format(percent_on))
            if self.stcpr_array:
                avg_duct_stcpr = mean(self.stcpr_array)
                # _log.debug("unocc_fan_operation ::: avg_duct_stcpr: {}".format(avg_duct_stcpr))

            for (key, unocc_time_thr), (key2, unocc_stcpr_thr) in thresholds:
                if percent_on > unocc_time_thr:
                    msg = "{} - Supply fan is on during unoccupied times".format(key)
                    # _log.debug("unocc_fan_operation ::: Supply fan is on during unoccupied times: percent_on_{} > unocc_time_thr{}".format(percent_on,unocc_time_thr))
                    result = 63.1
                else:
                    if avg_duct_stcpr < unocc_stcpr_thr:
                        msg = "{} - No problems detected for schedule diagnostic.".format(key)
                        # _log.debug("unocc_fan_operation ::: No problems detected for schedule diagnostic.: avg_duct_stcpr_{} > unocc_stcpr_thr{}".format(avg_duct_stcpr, unocc_stcpr_thr))
                        result = 60.0
                    else:
                        msg = ("{} - Fan status show the fan is off but the duct static "
                               "pressure is high, check the functionality of the "
                               "pressure sensor.".format(key))
                        # _log.debug("Fan status show the fan is off but the duct static "
                        #        "pressure is high, check the functionality of the "
                        #        "pressure sensor.")
                        result = 64.2
                diagnostic_msg.update({key: result})
                dx_result.log(msg)
        else:
            msg = "ALL - No problems detected for schedule diagnostic."
            dx_result.log(msg)
            diagnostic_msg = {"low": 60.0, "normal": 60.0, "high": 60.0}

        if 64.2 not in diagnostic_msg.values():
            # _log.debug("unocc_fan_operation ::: if 64.2 not in diagnostic_msg.values(): Entrance")
            for _hour in range(24):
                diagnostic_msg = {}
                utc_offset = self.timestamp_array[0].isoformat()[-6:]
                push_time = self.timestamp_array[0].date()
                push_time = datetime.combine(push_time, datetime.min.time())
                push_time = push_time.replace(hour=_hour)
                for key, unocc_time_thr in self.unocc_time_thr.items():
                    # _log.debug("unocc_fan_operation ::: if 64.2 not in diagnostic_msg.values(): self.unocc_time_thr: {}".format(self.unocc_time_thr))
                    diagnostic_msg.update({key: 60.0})
                    if hourly_counter[_hour] > unocc_time_thr:
                        # _log.debug("unocc_fan_operation ::: if 64.2 not in diagnostic_msg.values(): hourly_counter[_hour]_{} > unocc_time_thr_{}".format(hourly_counter[_hour],unocc_time_thr))
                        diagnostic_msg.update({key: 63.1})
                dx_table = {SCHED_RCX + DX:  diagnostic_msg}
                # _log.debug("unocc_fan_operation ::: if 64.2 not in diagnostic_msg.values(): dx_table: {}".format(dx_table))
                table_key = create_table_key(self.analysis, push_time) + utc_offset
                dx_result.insert_table_row(table_key, dx_table)
        else:
            push_time = self.timestamp_array[0].date()
            table_key = create_table_key(self.analysis, push_time)
            dx_result.insert_table_row(table_key, {SCHED_RCX + DX:  diagnostic_msg})

        return dx_result

    def no_static_pr_reset(self, dx_result):
        """
        AIRCx  to detect whether a static pressure set point reset is implemented.
        :param dx_result:
        :return:
        """
        # _log.debug("setpoint_reset_aircx ::: no_static_pr_reset Entrance success")
        diagnostic_msg = {}
        stcpr_daily_range = max(self.stcpr_stpt_array) - min(self.stcpr_stpt_array)
        # _log.debug("no_static_pr_reset ::: self.stcpr_stpt_array: {}".format(max(self.stcpr_stpt_array)))
        # _log.debug("no_static_pr_reset ::: self.stcpr_stpt_array: {}".format(min(self.stcpr_stpt_array)))
        # _log.debug("no_static_pr_reset ::: stcpr_daily_range: {}".format(stcpr_daily_range))
        # _log.debug("no_static_pr_reset ::: self.stcpr_reset_thr.items: {}".format(self.stcpr_reset_thr.items()))
        for sensitivity, stcpr_reset_thr in self.stcpr_reset_thr.items():
            if stcpr_daily_range < stcpr_reset_thr:
                # _log.debug("no_static_pr_reset ::: stcpr_daily_range {} < stcpr_reset_thr {} ".format(stcpr_daily_range,stcpr_reset_thr))
                msg = ("{} - No duct static pressure reset detected.".format(sensitivity))
                result = 71.1
            else:
                msg = ("{} - No problems detected for duct static pressure set point "
                       "reset diagnostic.".format(sensitivity))
                # _log.debug("No problems detected for duct static pressure set point "
                #        "reset diagnostic.")
                result = 70.0
            dx_result.log(msg)
            diagnostic_msg.update({sensitivity: result})

        dx_result.insert_table_row(self.reset_table_key, {DUCT_STC_RCX3 + DX:  diagnostic_msg})
        return dx_result

    def no_sat_stpt_reset(self, dx_result):
        """
        AIRCx to detect whether a supply-air temperature set point reset is implemented.
        :param dx_result:
        :return:
        """
        # _log.debug("setpoint_reset_aircx ::: no_sat_stpt_reset Entrance success")
        diagnostic_msg = {}
        sat_daily_range = max(self.sat_stpt_array) - min(self.sat_stpt_array)
        # _log.debug("no_sat_stpt_reset ::: self.stcpr_stpt_array: {}".format(max(self.sat_stpt_array)))
        # _log.debug("no_sat_stpt_reset ::: self.stcpr_stpt_array: {}".format(min(self.sat_stpt_array)))
        # _log.debug("no_sat_stpt_reset ::: stcpr_daily_range: {}".format(sat_daily_range))
        # _log.debug("no_sat_stpt_reset ::: self.stcpr_reset_thr.items: {}".format(self.sat_reset_thr.items()))
        for sensitivity, reset_thr in self.sat_reset_thr.items():
            if sat_daily_range < reset_thr:
                # _log.debug("no_sat_stpt_reset ::: sat_daily_range {} < reset_thr {} ".format(sat_daily_range,reset_thr))
                msg = "{} - SAT reset was not detected.".format(sensitivity)
                result = 81.1
            else:
                msg = "{} - No problems detected for SAT set point reset diagnostic.".format(sensitivity)
                # _log.debug("No problems detected for SAT set point reset diagnostic.")
                result = 80.0
            dx_result.log(msg)
            diagnostic_msg.update({sensitivity: result})

        dx_result.insert_table_row(self.reset_table_key, {SA_TEMP_RCX3 + DX:  diagnostic_msg})
        return dx_result
