#!/usr/bin/python
#
# Dumps relavent 'IAPD' XML data to csv file
# Requires 'bigxml'
#
# Notes:
# - IAPD's 'SEC Investment Advisor Report' was ~70MB XML as of 06/2023
# - only scrapes fields which author found useful
#
# Description of (most) fields captured:
#   part1a
#     item1
#       attr q1f5 - total number of offices other than principal office
#       attr q1O - over $1B in AUM
#     item2a
#       attr q2a1 - at least $90/$100M AUM
#     item3a
#       attr OrgFormNm - legal structure
#     item5a
#       attr TtlEmp - total employees
#     item5d
#       attr q5da1 - number of non-HNW clients
#       attr q5da3 - AUM of non-HNW clients
#       attr q5db1 - number of HNW clients
#       attr q5db3 - AUM of HNW clients
#     item5e
#       attr q5e1 - compensation: % of AUM
#       attr q5e2 - compensation: hourly charges
#       attr q5e3 - compensation: subscription fees
#       attr q5e4 - compensation: fixed fees
#       attr q5e5 - compensation: commissions
#       attr q5e6 - compensation: performance-based fees
#     item5f
#       q5f2A - discretionary AUM
#       q5f2B - non-discretionary AUM
#       q5f2C - total AUM
#       q5f2D - discretionary accounts
#       q5f2E - non-discretionary accounts
#       q5f2F - total accounts


import csv
import dataclasses
import sys

import bigxml

# Local path to "SEC Investment Advisers" XML file and output CSV file
# (Download XML file from here: https://adviserinfo.sec.gov/compilation)
INPUT_FILE = "IA_FIRM_SEC_Feed_11_06_2022.xml"
OUTPUT_FILE = "output.csv"


@bigxml.xml_handle_element("IAPDFirmSECReport", "Firms", "Firm")
@dataclasses.dataclass
class Entry:
    name: str = ""
    city: str = ""
    state: str = ""
    notices: str = ""
    org_type: str = ""
    offices: str = ""
    employees: str = "n/a"
    clients_indiv_count: str = ""
    clients_indiv_aum: str = ""
    clients_hnw_count: str = ""
    clients_hnw_aum: str = ""
    clients_pools_count: str = ""
    clients_pools_aum: str = ""
    clients_charitable_count: str = ""
    clients_charitable_aum: str = ""
    clients_corp_count: str = ""
    clients_corp_aum: str = ""
    advisory: str = ""
    compensation_percentage: str = ""
    compensation_hourly: str = ""
    compensation_subscription: str = ""
    compensation_fixed: str = ""
    compensation_commission: str = ""
    compensation_performance: str = ""
    compensation_other: str = ""
    aum_disc_dollars: str = ""
    aum_nondisc_dollars: str = ""
    aum_total_dollars: str = ""
    aum_disc_accounts: str = ""
    aum_nondisc_accounts: str = ""
    aum_total_accounts: str = ""
    has_trust_co: str = ""
    industry_brokerdealer: str = ""
    industry_planner: str = ""
    industry_trust: str = ""

    @bigxml.xml_handle_element("Info")
    def business_name(self, node):
        if "BusNm" in node.attributes:
            self.name = node.attributes["BusNm"]

    @bigxml.xml_handle_element("MainAddr")
    def headquarters(self, node):
        if "City" in node.attributes:
            self.city = node.attributes["City"]
        if "State" in node.attributes:
            self.state = node.attributes["State"]

    @bigxml.xml_handle_element("NoticeFiled", "States")
    def noticesx(self, node):
        if "RgltrCd" in node.attributes:
            self.notices += node.attributes["RgltrCd"] + ","

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item1")
    def officesx(self, node):
        if "Q1F5" in node.attributes:
            self.offices = node.attributes["Q1F5"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item3A")
    def org_typex(self, node):
        if "OrgFormNm" in node.attributes:
            self.org_type = node.attributes["OrgFormNm"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item5A")
    def employeesx(self, node):
        if "TtlEmp" in node.attributes:
            self.employees = node.attributes["TtlEmp"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item5D")
    def clientsx(self, node):
        if "Q5DA1" in node.attributes:
            self.clients_indiv_count = node.attributes["Q5DA1"]
        if "Q5DA3" in node.attributes:
            self.clients_indiv_aum = node.attributes["Q5DA3"]
        if "Q5DB1" in node.attributes:
            self.clients_hnw_count = node.attributes["Q5DB1"]
        if "Q5DB3" in node.attributes:
            self.clients_hnw_aum = node.attributes["Q5DB3"]
        if "Q5DF1" in node.attributes:
            self.clients_pools_count = node.attributes["Q5DF1"]
        if "Q5DF3" in node.attributes:
            self.clients_pools_aum = node.attributes["Q5DF3"]
        if "Q5DH1" in node.attributes:
            self.clients_charitable_count = node.attributes["Q5DH1"]
        if "Q5DH3" in node.attributes:
            self.clients_charitable_aum = node.attributes["Q5DH3"]
        if "Q5DM1" in node.attributes:
            self.clients_corp_count = node.attributes["Q5DM1"]
        if "Q5DM3" in node.attributes:
            self.clients_corp_aum = node.attributes["Q5DM3"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item5E")
    def compensationx(self, node):
        if "Q5E1" in node.attributes:
            self.compensation_percentage = node.attributes["Q5E1"]
        if "Q5E2" in node.attributes:
            self.compensation_hourly = node.attributes["Q5E2"]
        if "Q5E3" in node.attributes:
            self.compensation_subscription = node.attributes["Q5E3"]
        if "Q5E4" in node.attributes:
            self.compensation_fixed = node.attributes["Q5E4"]
        if "Q5E5" in node.attributes:
            self.compensation_commission = node.attributes["Q5E5"]
        if "Q5E6" in node.attributes:
            self.compensation_performance = node.attributes["Q5E6"]
        if "Q5E7" in node.attributes:
            self.compensation_other = node.attributes["Q5E7"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item5F")
    def aumx(self, node):
        if "Q5F2A" in node.attributes:
            self.aum_disc_dollars = node.attributes["Q5F2A"]
        if "Q5F2B" in node.attributes:
            self.aum_nondisc_dollars = node.attributes["Q5F2B"]
        if "Q5F2C" in node.attributes:
            self.aum_total_dollars = node.attributes["Q5F2C"]
        if "Q5F2D" in node.attributes:
            self.aum_disc_accounts = node.attributes["Q5F2D"]
        if "Q5F2E" in node.attributes:
            self.aum_nondisc_accounts = node.attributes["Q5F2E"]
        if "Q5F2F" in node.attributes:
            self.aum_total_accounts = node.attributes["Q5F2F"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item5G")
    def advisoryx(self, node):
        if "Q5G1" in node.attributes:
            self.advisory = node.attributes["Q5G1"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item6A")
    def other_businessx(self, node):
        if "Q6A8" in node.attributes:
            self.has_trust_co = node.attributes["Q6A8"]

    @bigxml.xml_handle_element("FormInfo", "Part1A", "Item7A")
    def industry_affiliationsx(self, node):
        if "Q7A1" in node.attributes:
            self.industry_brokerdealer = node.attributes["Q7A1"]
        if "Q7A2" in node.attributes:
            self.industry_planner = node.attributes["Q7A2"]
        if "Q7A9" in node.attributes:
            self.industry_trust = node.attributes["Q7A9"]


with open(sys.argv[2], "w") as w:
    writer = csv.writer(w, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    with open(sys.argv[1], "rb") as f:
        writer.writerow(["Firm: Name"]
                        + ["Firm: Notices"]
                        + ["Firm: Org type"]
                        + ["Firm: # Offices"]
                        + ["Firm: # Employees"]
                        + ["Firm: HQ State"]
                        + ["Firm: HQ City"]
                        + ["Clients: Indiv"]
                        + ["Clients: Indiv AUM"]
                        + ["Clients: HNW"]
                        + ["Clients: HNW AUM"]
                        + ["Clients: Charitable"]
                        + ["Clients: Charitable AUM"]
                        + ["Clients: Corporate"]
                        + ["Clients: Corporate AUM"]
                        + ["Financil planning?"]
                        + ["Comp: %"]
                        + ["Comp: Hourly"]
                        + ["Comp: Subscription"]
                        + ["Comp: Fixed"]
                        + ["Comp: Commission"]
                        + ["Comp: Performance"]
                        + ["Comp: Other"]
                        + ["AUM: Discretionary"]
                        + ["AUM: Discretionary AUM"]
                        + ["AUM: Non-discretionary"]
                        + ["AUM: Non-discretionary AUM"]
                        + ["AUM: Total"]
                        + ["AUM: Total AUM"]
                        + ["Industry: Has Trust Co."]
                        + ["Industry: Broker-dealer"]
                        + ["Industry: Other planner"]
                        + ["Industry: Trust co."]

                        )
        for item in bigxml.Parser(f).iter_from(Entry):
            if "Y" in item.advisory:
                writer.writerow([str(item.name)]
                                + [str(item.notices)]
                                + [str(item.org_type)]
                                + [str(item.offices)]
                                + [str(item.employees)]
                                + [str(item.state)]
                                + [str(item.city)]
                                + [str(item.clients_indiv_count)]
                                + [str(item.clients_indiv_aum)]
                                + [str(item.clients_hnw_count)]
                                + [str(item.clients_hnw_aum)]
                                + [str(item.clients_charitable_count)]
                                + [str(item.clients_charitable_aum)]
                                + [str(item.clients_corp_count)]
                                + [str(item.clients_corp_aum)]
                                + [str(item.advisory)]
                                + [str(item.compensation_percentage)]
                                + [str(item.compensation_hourly)]
                                + [str(item.compensation_subscription)]
                                + [str(item.compensation_fixed)]
                                + [str(item.compensation_commission)]
                                + [str(item.compensation_performance)]
                                + [str(item.compensation_other)]
                                + [str(item.aum_disc_accounts)]
                                + [str(item.aum_disc_dollars)]
                                + [str(item.aum_nondisc_accounts)]
                                + [str(item.aum_nondisc_dollars)]
                                + [str(item.aum_total_accounts)]
                                + [str(item.aum_total_dollars)]
                                + [str(item.has_trust_co)]
                                + [str(item.industry_brokerdealer)]
                                + [str(item.industry_planner)]
                                + [str(item.industry_trust)]
                                )
