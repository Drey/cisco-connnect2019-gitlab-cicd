*** Settings ***

Library         ats.robot.pyATSRobot
Library         genie.libs.robot.GenieRobot
Library         unicon.robot.UniconRobot

*** Test Cases ***

Loading testbed
    [Tags]  base
    use genie testbed "%{NXOS_TESTBED}"
Connecting to device
    [Tags]  base
    connect to devices "%{NXOS_DEVICE}"
Verify vPC domain status
	[Tags]	system
	verify vpc status on device "%{NXOS_DEVICE}"
Verify underlay interfaces
    [Tags]	underlay
    verify interface list "%{NXOS_UNDERLAY_IF_LIST}" status "up" on device "%{NXOS_DEVICE}"
Verify OSPF underlay
    [Tags]	underlay
    verify count "3" "ospf neighbors" on device "%{NXOS_DEVICE}"
Verify PIM underlay
    [Tags]	underlay
    verify count "3" "pim neighbors" on device "%{NXOS_DEVICE}"
Verify MP-BGP overlay
    [Tags]	overlay
    verify count "2" "bgp neighbors" on device "%{NXOS_DEVICE}"
Verify VXLAN & EVPN l2vni services
    [Tags]	services
    verify evpn "l2vni" service list "%{NXOS_EVPN_L2VNI_LIST}" on device "%{NXOS_DEVICE}"
Verify VXLAN & EVPN l3vni services
    [Tags]	services
    verify evpn "l3vni" service list "%{NXOS_EVPN_L3VNI_LIST}" on device "%{NXOS_DEVICE}"
