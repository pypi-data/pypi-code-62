from time import time

from paradox.event import EventLevel


def _toggle_provider(old):
    return not old


def _timestamp_provider(old):
    return int(time())


event_opt1 = {
    1: dict(type="output", id=1),
    2: dict(type="output", id=2),
    3: dict(type="output", id=3),
    4: dict(type="output", id=4),
    5: dict(type="output", id=5),
    6: dict(type="output", id=6),
    7: dict(type="output", id=7),
    8: dict(type="output", id=8),
    9: dict(type="output", id=9),
    10: dict(type="output", id=10),
    11: dict(type="output", id=11),
    12: dict(type="output", id=12),
    13: dict(type="output", id=13),
    14: dict(type="output", id=14),
    15: dict(type="output", id=15),
    16: dict(type="output", id=16),
    17: dict(type="repeater", id=1),
    18: dict(type="repeater", id=2),
    19: dict(type="keypad", id=1),
    20: dict(type="keypad", id=2),
    21: dict(type="keypad", id=3),
    22: dict(type="keypad", id=4),
    27: dict(type="siren", id=1),
    28: dict(type="siren", id=2),
    29: dict(type="siren", id=3),
    30: dict(type="siren", id=4),
    99: dict(),
}

event_map = {
    0: dict(
        level=EventLevel.DEBUG,
        change=dict(open=False),
        type="zone",
        message="Zone {label} OK",
    ),
    1: dict(
        level=EventLevel.DEBUG,
        change=dict(open=True),
        type="zone",
        message="Zone {label} open",
    ),
    2: dict(
        level=EventLevel.CRITICAL,
        type="partition",
        sub={
            0: dict(message="N/A"),
            1: dict(message="N/A"),
            2: dict(
                change=dict(silent_alarm=True, alarm=True),
                tags=["alarm", "silent_alarm"],
                message="Partition {label} silent alarm active",
            ),
            3: dict(
                change=dict(audible_alarm=True, alarm=True),
                tags=["alarm", "buzzer_alarm"],
                message="Partition {label} buzzer alarm active",
            ),
            4: dict(
                change=dict(audible_alarm=True, alarm=True),
                tags=["alarm", "steady_alarm"],
                message="Partition {label} steady alarm active",
            ),
            5: dict(
                change=dict(audible_alarm=True, alarm=True),
                tags=["alarm", "pulse_alarm"],
                message="Partition {label} pulse alarm active",
            ),
            6: dict(
                change=dict(strobe_alarm=True, alarm=True),
                tags=["alarm", "strobe"],
                message="Partition {label} strobe active",
            ),
            7: dict(
                level=EventLevel.INFO,
                change=dict(alarm=False),
                message="Partition {label} alarm stopped",
            ),
            8: dict(
                level=EventLevel.DEBUG,
                change=dict(squawk=True),
                id=1,
                message="Squawk ON",
            ),
            9: dict(
                level=EventLevel.DEBUG,
                change=dict(squawk=False),
                id=1,
                message="Squawk OFF",
            ),
            10: dict(level=EventLevel.DEBUG, message="Ground Start"),
            11: dict(
                level=EventLevel.INFO,
                change=dict(arm=False, arm_sleep=False, arm_stay=False, alarm=False),
                tags=["disarm"],
                message="Partition {label} disarmed",
            ),
            12: dict(
                level=EventLevel.INFO,
                change=dict(arm=True),
                tags=["arm"],
                message="Partition {label} armed",
            ),
            13: dict(
                level=EventLevel.INFO,
                change=dict(entry_delay=True),
                message="Partition {label} in entry delay",
            ),
            14: dict(
                level=EventLevel.INFO,
                change=dict(exit_delay=True),
                message="Partition {label} in exit delay",
            ),
            15: dict(level=EventLevel.DEBUG, message="Pre-alarm delay"),
            16: dict(level=EventLevel.DEBUG, message="Report confirmation"),
            99: dict(level=EventLevel.DEBUG, message="Any partition status event"),
        },
    ),
    3: dict(
        level=EventLevel.DEBUG,
        type="system",
        sub={
            0: dict(change=dict(bell_activated=False), message="Bell OFF"),
            1: dict(change=dict(bell_activated=True), message="Bell ON"),
            2: dict(message="Bell squawk arm"),
            3: dict(message="Bell squawk disarm"),
            99: dict(message="Any bell status event"),
        },
    ),
    # 5: 'Non-Reportable Event',
    6: dict(
        level=EventLevel.DEBUG,
        message="Non-reportable event",
        sub={
            0: dict(
                level=EventLevel.CRITICAL,
                type="system",
                tags=["trouble"],
                message="Telephone line trouble",
            ),
            1: dict(type="system", message="[ENTER]/[CLEAR]/[POWER] key was pressed"),
            2: dict(message="N/A"),
            3: dict(
                level=EventLevel.INFO,
                change=dict(arm_stay=True, arm=True),
                type="partition",
                tags=["arm"],
                message="Arm in stay mode",
            ),
            4: dict(
                level=EventLevel.INFO,
                change=dict(arm_sleep=True, arm=True),
                type="partition",
                tags=["arm"],
                message="Arm in sleep mode",
            ),
            5: dict(
                level=EventLevel.INFO,
                change=dict(arm_force=True, arm=True),
                type="partition",
                tags=["arm"],
                message="Arm in force mode",
            ),
            6: dict(
                level=EventLevel.INFO,
                change=dict(arm_stay=True, arm=True),
                type="partition",
                tags=["arm"],
                message="Full arm when armed in stay mode",
            ),
            7: dict(
                level=EventLevel.CRITICAL,
                tags=["trouble"],
                change=dict(computer_fail_to_communicate_trouble=True),
                type="system",
                message="PC fail to communicate",
            ),
            8: dict(type="system", message="Utility Key 1 pressed (keys [1] and [2])"),
            9: dict(type="system", message="Utility Key 2 pressed (keys [4] and [5])"),
            10: dict(type="system", message="Utility Key 3 pressed (keys [7] and [8])"),
            11: dict(type="system", message="Utility Key 4 pressed (keys [2] and [3])"),
            12: dict(type="system", message="Utility Key 5 pressed (keys [5] and [6])"),
            13: dict(type="system", message="Utility Key 6 pressed (keys [8] and [9])"),
            14: dict(
                level=EventLevel.CRITICAL,
                type="system",
                tags=["alarm"],
                message="Tamper generated alarm",
            ),
            15: dict(
                level=EventLevel.CRITICAL,
                type="system",
                tags=["supervision", "alarm"],
                message="Supervision loss generated alarm",
            ),
            16: dict(message="N/A"),
            17: dict(message="N/A"),
            18: dict(message="N/A"),
            19: dict(message="N/A"),
            20: dict(
                level=EventLevel.INFO,
                change=dict(arm=True),
                type="partition",
                message="Full arm when armed in sleep mode",
            ),
            21: dict(type="firmware", message="Firmware upgrade"),
            22: dict(message="N/A"),
            23: dict(
                change=dict(stayd_mode_active=True),
                type="partition",
                message="StayD mode activated",
            ),
            24: dict(
                change=dict(stayd_mode_active=False),
                type="partition",
                message="StayD mode deactivated",
            ),
            25: dict(type="system", message="IP Registration status change"),
            26: dict(type="system", message="GPRS Registration status change"),
            27: dict(
                level=EventLevel.INFO, type="partition", message="Armed with trouble(s)"
            ),
            28: dict(
                level=EventLevel.WARN,
                type="system",
                tags=["trouble", "supervision"],
                message="Supervision alert",
            ),
            29: dict(
                level=EventLevel.INFO,
                type="system",
                tags=["trouble", "restore", "supervision"],
                message="Supervision alert restore",
            ),
            30: dict(
                level=EventLevel.WARN,
                type="partition",
                message="Armed with remote with low battery",
            ),
            99: dict(message="Any non-reportable event"),
        },
    ),
    # 7: 'PGM Activation',
    8: dict(
        level=EventLevel.DEBUG,
        type="user",
        change=dict(button_b=_timestamp_provider),
        message="Button B pressed on remote of {@user}",
    ),
    9: dict(
        level=EventLevel.DEBUG,
        type="user",
        change=dict(button_c=_timestamp_provider),
        message="Button C pressed on remote of {@user}",
    ),
    10: dict(
        level=EventLevel.DEBUG,
        type="user",
        change=dict(button_d=_timestamp_provider),
        message="Button D pressed on remote of {@user}",
    ),
    11: dict(
        level=EventLevel.DEBUG,
        type="user",
        change=dict(button_e=_timestamp_provider),
        message="Button E pressed on remote of {@user}",
    ),
    12: dict(
        level=EventLevel.DEBUG, type="user", message="Cold start wireless zone {label}"
    ),
    13: dict(
        level=EventLevel.DEBUG,
        type="user",
        message="Cold start wireless module {label}",
    ),
    14: dict(
        level=EventLevel.DEBUG,
        type="zone",
        change=dict(bypassed=_toggle_provider),
        message="Bypass programming on zone {label}",
    ),
    15: dict(
        level=EventLevel.DEBUG,
        type="partition",
        message="User code activated output {label}",
    ),
    16: dict(
        level=EventLevel.DEBUG, type="zone", message="Wireless smoke maintenance signal"
    ),
    17: dict(
        level=EventLevel.DEBUG,
        type="zone",
        message="Delay zone {label} alarm transmission",
    ),
    18: dict(
        level=EventLevel.WARN,
        type="zone",
        message="Zone {label} signal strength weak 1",
    ),
    19: dict(
        level=EventLevel.WARN,
        type="zone",
        message="Zone {label} signal strength weak 2",
    ),
    20: dict(
        level=EventLevel.WARN,
        type="zone",
        message="Zone {label} signal strength weak 3",
    ),
    21: dict(
        level=EventLevel.WARN,
        type="zone",
        message="Zone {label} signal strength weak 4",
    ),
    22: dict(
        level=EventLevel.DEBUG,
        type="user",
        change=dict(button_5=_timestamp_provider),
        message="Button 5 pressed on remote of {@user}",
    ),
    23: dict(
        level=EventLevel.DEBUG,
        type="user",
        change=dict(button_6=_timestamp_provider),
        message="Button 6 pressed on remote of {@user}",
    ),
    24: dict(
        level=EventLevel.WARN,
        type="zone",
        change=dict(fire_delay=True),
        message="Fire delay started",
    ),
    # 25: 'N/A',
    26: dict(
        level=EventLevel.DEBUG,
        type="system",
        message="Software access",
        sub={
            0: dict(message="Non-valid source ID"),
            1: dict(message="WinLoad direct"),
            2: dict(message="WinLoad through IP module"),
            3: dict(message="WinLoad through GSM module"),
            4: dict(message="WinLoad through modem"),
            9: dict(message="IP100 direct"),
            10: dict(message="VDMP3 direct"),
            11: dict(message="Voice through GSM module"),
            12: dict(message="Remote access"),
            13: dict(message="SMS through GSM module"),
            99: dict(message="Any software access"),
        },
    ),
    27: dict(
        level=EventLevel.DEBUG,
        type="bus",
        message="Bus module event",
        sub={
            0: dict(message="A bus module was added"),
            1: dict(message="A bus module was removed"),
            2: dict(message="2-way RF Module Communication Failure"),
            3: dict(message="2-way RF Module Communication Restored"),
        },
    ),
    28: dict(
        level=EventLevel.INFO,
        type="zone",
        message="StayD pass acknowledged for {label}",
    ),
    29: dict(
        level=EventLevel.INFO,
        type="user",
        tags=["arm"],
        message="Arming by user {label}",
    ),
    30: dict(
        level=EventLevel.INFO,
        type="special",
        message="Special arming",
        sub={
            0: dict(tags=["arm"], message="Auto-arming (on time/no movement)"),
            1: dict(message="Late to close"),
            2: dict(tags=["arm"], message="No movement arming"),
            3: dict(tags=["arm"], message="Partial arming"),
            4: dict(tags=["arm"], message="Quick arming"),
            5: dict(tags=["arm"], message="Arming through WinLoad"),
            6: dict(tags=["arm"], message="Arming with keyswitch"),
            99: dict(tags=["arm"], message="Any special arming"),
        },
    ),
    31: dict(
        level=EventLevel.INFO,
        type="user",
        tags=["disarm"],
        message="Disarming by user {label}",
    ),
    32: dict(
        level=EventLevel.INFO,
        type="user",
        tags=["disarm", "after_alarm"],
        message="Disarming after alarm by user {label}",
    ),
    33: dict(
        level=EventLevel.INFO,
        type="user",
        tags=["alarm", "cancel"],
        message="Alarm cancelled by user {label}",
    ),
    34: dict(
        level=EventLevel.WARN,
        type="special",
        sub={
            0: dict(message="Auto-arm cancelled (on time/no movement)"),
            1: dict(
                level=EventLevel.INFO,
                tags=["disarm"],
                message="Disarming through WinLoad",
            ),
            2: dict(
                level=EventLevel.INFO,
                tags=["disarm", "after_alarm"],
                message="Disarming through WinLoad after alarm",
            ),
            3: dict(
                level=EventLevel.INFO,
                tags=["alarm", "cancel"],
                message="Alarm cancelled through WinLoad",
            ),
            4: dict(
                level=EventLevel.INFO,
                tags=["alarm", "cancel"],
                message="Paramedical alarm cancelled",
            ),
            5: dict(
                level=EventLevel.DEBUG, tags=["disarm"], message="Disarm with keyswitch"
            ),
            6: dict(
                level=EventLevel.DEBUG,
                tags=["disarm", "after_alarm"],
                message="Disarm with keyswitch after an alarm",
            ),
            7: dict(
                level=EventLevel.INFO,
                tags=["alarm", "cancel"],
                message="Alarm cancelled with keyswitch",
            ),
            99: dict(
                level=EventLevel.INFO, tags=["disarm"], message="Any special disarming"
            ),
        },
    ),
    35: dict(
        level=EventLevel.INFO,
        change=dict(bypassed=_toggle_provider),
        type="zone",
        tags=["bypass"],
        message="Zone {label} bypass toggled",
    ),
    36: dict(
        level=EventLevel.CRITICAL,
        change=dict(alarm=True),
        type="zone",
        tags=["alarm", "trigger"],
        message="Zone {label} in alarm",
    ),
    37: dict(
        level=EventLevel.CRITICAL,
        change=dict(fire_alarm=True),
        type="zone",
        tags=["alarm", "fire", "trigger"],
        message="Zone {label} in fire alarm",
    ),
    38: dict(
        level=EventLevel.CRITICAL,
        change=dict(alarm=False),
        type="zone",
        tags=["alarm", "restore"],
        message="Zone {label} alarm restore",
    ),
    39: dict(
        level=EventLevel.CRITICAL,
        change=dict(fire_alarm=False),
        type="zone",
        tags=["alarm", "fire", "restore"],
        message="Zone {label} fire alarm restore",
    ),
    40: dict(
        level=EventLevel.CRITICAL,
        type="special",
        tags=["alarm", "trigger"],
        message="Special alarm",
        sub={
            0: dict(message="Panic non-medical emergency"),
            1: dict(message="Panic medical"),
            2: dict(message="Panic fire"),
            3: dict(message="Recent closing"),
            4: dict(message="Global shutdown"),
            5: dict(message="Duress alarm"),
            6: dict(message="Keypad lockout"),
            99: dict(message="Any special alarm event"),
        },
    ),
    41: dict(
        level=EventLevel.INFO,
        change=dict(shutdown=True),
        type="zone",
        message="Zone {label} shutdown",
    ),
    42: dict(
        level=EventLevel.WARN,
        change=dict(zone_tamper_trouble=True),
        tags=["tamper"],
        type="zone",
        message="Zone {label} tampered",
    ),
    43: dict(
        level=EventLevel.INFO,
        change=dict(zone_tamper_trouble=False),
        tags=["tamper", "restore"],
        type="zone",
        message="Zone {label} tamper restore",
    ),
    44: dict(
        level=EventLevel.WARN,
        type="system",
        tags=["trouble"],
        sub={
            0: dict(message="N/A"),
            1: dict(message="AC failure"),
            2: dict(message="Battery failure"),
            3: dict(message="Auxiliary current overload"),
            4: dict(message="Bell current overload"),
            5: dict(message="Bell disconnected"),
            6: dict(change=dict(timer_loss_trouble=True), message="Clock loss"),
            7: dict(change=dict(fire_loop_trouble=True), message="Fire loop trouble"),
            8: dict(message="Fail to communicate to monitoring station telephone #1"),
            9: dict(message="Fail to communicate to monitoring station telephone #2"),
            11: dict(message="Fail to communicate to voice report"),
            12: dict(message="RF jamming"),
            13: dict(message="GSM RF jamming"),
            14: dict(message="GSM no service"),
            15: dict(message="GSM supervision lost"),
            16: dict(message="Fail To Communicate IP Receiver 1 (GPRS)"),
            17: dict(message="Fail To Communicate IP Receiver 2 (GPRS)"),
            18: dict(message="IP Module No Service"),
            19: dict(message="IP Module Supervision Loss"),
            20: dict(message="Fail To Communicate IP Receiver 1 (IP)"),
            21: dict(message="Fail To Communicate IP Receiver 2 (IP)"),
            99: dict(message="Any new trouble event"),
        },
    ),
    45: dict(
        level=EventLevel.INFO,
        type="system",
        tags=["trouble", "restore"],
        sub={
            0: dict(message="Telephone line restore"),
            1: dict(message="AC failure restore"),
            2: dict(message="Battery failure restore"),
            3: dict(message="Auxiliary current overload restore"),
            4: dict(message="Bell current overload restore"),
            5: dict(message="Bell disconnected restore"),
            6: dict(message="Clock loss restore"),
            7: dict(message="Fire loop trouble restore"),
            8: dict(
                message="Fail to communicate to monitoring station telephone #1 restore"
            ),
            9: dict(
                message="Fail to communicate to monitoring station telephone #2 restore"
            ),
            11: dict(message="Fail to communicate to voice report restore"),
            12: dict(message="RF jamming restore"),
            13: dict(message="GSM RF jamming restore"),
            14: dict(message="GSM no service restore"),
            15: dict(message="GSM supervision lost restore"),
            16: dict(message="Fail To Communicate IP Receiver 1 (GPRS) restore"),
            17: dict(message="Fail To Communicate IP Receiver 2 (GPRS) restore"),
            18: dict(message="IP Module No Service restore"),
            19: dict(message="IP Module Supervision Loss restore"),
            20: dict(message="Fail To Communicate IP Receiver 1 (IP) restore"),
            21: dict(message="Fail To Communicate IP Receiver 2 (IP) restore"),
            99: dict(message="Any trouble event restore"),
        },
    ),
    46: dict(
        level=EventLevel.WARN,
        type="module",
        tags=["trouble"],
        sub={
            0: dict(message="Bus / EBus / Wireless module communication fault"),
            1: dict(message="Tamper trouble"),
            2: dict(message="Power fail"),
            3: dict(message="Battery failure"),
            99: dict(message="Any bus module new trouble event"),
        },
    ),
    47: dict(
        level=EventLevel.INFO,
        type="system",
        tags=["trouble", "restore"],
        sub={
            0: dict(message="Bus / EBus / Wireless module communication fault restore"),
            1: dict(message="Tamper trouble restore"),
            2: dict(message="Power fail restore"),
            3: dict(message="Battery failure restore"),
            99: dict(message="Any bus module trouble restored event"),
        },
    ),
    48: dict(
        level=EventLevel.INFO,
        type="system",
        sub={
            0: dict(message="System power up"),
            1: dict(message="Reporting test"),
            2: dict(message="Software log on"),
            3: dict(message="Software log off"),
            4: dict(message="Installer in programming mode"),
            5: dict(message="Installer exited programming mode"),
            6: dict(message="Maintenance in programming mode"),
            7: dict(message="Maintenance exited programming mode"),
            8: dict(message="Closing delinquency delay elapsed"),
            99: dict(message="Any special event"),
        },
    ),
    49: dict(
        level=EventLevel.WARN,
        changes=dict(zone_rf_low_battery_trouble=True),
        type="zone",
        tags=["trouble"],
        message="Low battery on zone {label}",
    ),
    50: dict(
        level=EventLevel.INFO,
        changes=dict(zone_rf_low_battery_trouble=False),
        type="zone",
        tags=["trouble", "restore"],
        message="Low battery on zone {label} restore",
    ),
    51: dict(
        level=EventLevel.WARN,
        changes=dict(zone_supervision_trouble=True),
        type="zone",
        tags=["trouble", "supervision"],
        message="Zone {label} supervision trouble",
    ),
    52: dict(
        level=EventLevel.INFO,
        changes=dict(zone_supervision_trouble=False),
        type="zone",
        tags=["trouble", "supervision", "restore"],
        message="Zone {label} supervision restore",
    ),
    53: dict(
        level=EventLevel.WARN,
        change=dict(module_supervision_trouble=True),
        type="module",
        tags=["trouble", "supervision"],
        message="Wireless module {label} supervision trouble",
        sub=event_opt1,
    ),
    54: dict(
        level=EventLevel.INFO,
        change=dict(module_supervision_trouble=False),
        type="module",
        tags=["trouble", "supervision", "restore"],
        message="Wireless module {label} supervision restore",
        sub=event_opt1,
    ),
    55: dict(
        level=EventLevel.WARN,
        change=dict(module_tamper_trouble=True),
        type="module",
        tags=["trouble", "tamper"],
        message="Wireless module {label} tamper trouble",
        sub=event_opt1,
    ),
    56: dict(
        level=EventLevel.INFO,
        change=dict(module_tamper_trouble=False),
        type="module",
        tags=["trouble", "tamper", "restore"],
        message="Wireless module {label} tamper restore",
    ),
    57: dict(
        level=EventLevel.CRITICAL,
        type="user",
        tags=["alarm", "medic", "trigger"],
        message="Non-medical alarm (paramedic) by {label}",
    ),
    58: dict(level=EventLevel.DEBUG, type="zone", message="Zone {label} forced"),
    59: dict(level=EventLevel.DEBUG, type="zone", message="Zone {label} included"),
    64: dict(
        level=EventLevel.DEBUG,
        type="system",
        sub={
            0: dict(message="Follow Arm LED status"),
            1: dict(message="PGM pulse fast in alarm"),
            2: dict(message="PGM pulse fast in exit delay below 10 sec."),
            3: dict(message="PGM pulse slow in exit delay over 10 sec."),
            4: dict(message="PGM steady ON if armed"),
            5: dict(message="PGM OFF if disarmed"),
        },
    ),
}

_labels = {
    "zone": "Zone Number {label}",
    "pgm": "PGM Number {label}",
    "user": "User {label}",
    "keypad": "Wireless Keypad {label}",
    "repeater": "Wireless Repeater {label}",
    "siren": "Wireless Siren {label}",
}
