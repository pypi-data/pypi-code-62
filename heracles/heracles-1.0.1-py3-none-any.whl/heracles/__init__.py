import subprocess
import sys
import uiautomator2 as u2
import tkinter as tk
from tkinter import ttk, messagebox
from airtest.cli.parser import cli_setup
from airtest.core.api import *


def getprop_check(android_property) -> str:  # returns string 'user' or 'eng'
    """Checks property value on device. Parses the result from 'getprop' command"""
    dut = u2.connect()
    getprop_value = dut.shell(
        'getprop '
        + str(android_property))[0]  # gets output, ignores exit_code
    getprop_value = getprop_value.replace("\n", "")  # returns string without 'newline' character
    return getprop_value


def airplane_mode_on():
    """Enables airplane mode on device. Uses broadcast or user interface according to build-type property"""
    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        dut.shell(r'am start -S com.android.settings/.Settings\$AirplaneModeSettingsActivity')
        dut.wait_activity('.Settings$AirplaneModeSettingsActivity')
        switch_airplane_mode = dut(className='android.widget.Switch')

        if not switch_airplane_mode.info['checked']:
            switch_airplane_mode.click()

        dut.shell('input keyevent KEYCODE_HOME')

    if getprop_check('ro.build.type') == 'eng':
        dut.shell('settings put global airplane_mode_on 1')
        dut.shell('am broadcast -f 268435456 -a android.intent.action.AIRPLANE_MODE --ez state true')


def airplane_mode_off():
    """Disables airplane mode on device. Uses broadcast or user interface according to build-type property"""
    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        dut.shell(r'am start -S com.android.settings/.Settings\$AirplaneModeSettingsActivity')
        dut.wait_activity('.Settings$AirplaneModeSettingsActivity')
        switch_airplane_mode = dut(className='android.widget.Switch')

        if switch_airplane_mode.info['checked']:
            switch_airplane_mode.click()

        dut.shell('input keyevent KEYCODE_HOME')

    if getprop_check('ro.build.type') == 'eng':
        dut.shell('settings put global airplane_mode_on 0')
        dut.shell('am broadcast -f 268435456 -a android.intent.action.AIRPLANE_MODE --ez state true')


def reboot():
    """Reboots the device. Equivalent to 'adb shell reboot'"""
    dut = u2.connect()
    dut.shell('reboot')


def call_answer():
    """Answers MT call in device.

    If the command is passed without arguments, simulates a 'call answer' key press

    If the command is passed with a single argument (voice, video, rtt), answers the call accordingly

    Args:
        "voice", "video", "rtt"

    Todo:
        Use default parameters

    """
    dut = u2.connect()

    # if command is invoked without parameters, perform a simple answer
    if len(sys.argv) == 1:
        dut.shell("input keyevent KEYCODE_CALL")

    # if one parameter, answer by call type
    # TODO: break in individual functions to improve readability
    if len(sys.argv) == 2:
        call_type = str(sys.argv[1])
        if call_type == "voice":
            if dut(descriptionMatches="(?i)(.*)answer voice call(.*)|(?i)null, null(.*)").exists(timeout=3):
                dut(descriptionMatches="(?i)(.*)answer voice call(.*)|(?i)null, null(.*)").drag_to(0.5, 0.5)
            else:
                dut.shell("input keyevent KEYCODE_CALL")
        elif call_type == "video":
            if dut(descriptionMatches="(?i)(.*)answer video call(.*)").exists(timeout=2):
                dut(descriptionMatches="(?i)(.*)answer video call(.*)").drag_to(0.5, 0.5)
        elif call_type == "rtt":
            if dut(descriptionMatches="(?i)(.*)drag right with two fingers to answer call(.*)").exists(timeout=3):
                dut(descriptionMatches="(?i)(.*)drag right with two fingers to answer call(.*)").drag_to(0.5, 0.5)
            else:
                # perform swipe via image recognition (airtest)
                if not cli_setup():
                    auto_setup(__file__, logdir=True, devices=[
                        "Android:///",
                    ], project_root="C:/PreSMCAutomationDraft")  # default folder location
                    swipe(
                        Template(
                            r"rtt_drag_button_android_Q.png",
                            record_pos=(-0.304, 0.666),  # TODO: get positional parameters from getprop or u2 library
                            resolution=(1080, 2400)
                        ),
                        vector=[0.3074, -0.2653])
        else:
            dut.shell("input keyevent KEYCODE_CALL")

    dut(textContains="on hold").click_exists(timeout=2.0)


def call_end():
    """Ends current call on device. Checks for emergency calls"""
    dut = u2.connect()
    dut.screen_on()  # screen is turned off while answering calls in some devices

    if dut(textMatches="(?i)(.*)emergency(.*)").exists():  # check for emergency call
        dut(resourceIdMatches="(?i)(.*)disconnect(.*)").click()  # emergency calls usually can't be ended via key press

    else:
        dut.shell("input keyevent KEYCODE_ENDCALL")


def call_initiate(call_type='voice', phone_number='1234321'):
    """Initiates MO call in device.

    If the command is passed without arguments, initiates a voice call to default number ('1234321')
    If only the call type is provided, makes a call of the specified type to the default number
    If only the phone number is provided, makes a voice call to the specified phone number
    If the phone number is an emergency number, defaults to a emergency call

    Args:
        call_type (str): voice, video, rtt
        phone_number (str): phone number

    """
    dut = u2.connect()

    if phone_number in ['911', '711']:  # check for emergency numbers
        if getprop_check('ro.build.type') == 'user':
            dut.shell(
                'am start -a android.intent.action.DIAL -d tel:'
                + phone_number
            )
            dut.shell("input keyevent KEYCODE_CALL")
        elif getprop_check('ro.build.type') == 'eng':
            dut.shell(
                'am start -a android.intent.action.CALL_PRIVILEGED -d tel:'
                + phone_number
            )

    elif call_type == 'voice':
        dut.shell(
            'am start -a android.intent.action.CALL -d tel:'
            + phone_number
        )
    elif call_type == 'video':
        if getprop_check('ro.build.version.sdk') == '29':  # Android 10
            dut.shell(
                'am start -a android.intent.action.DIAL -d tel:'
                + phone_number
            )
            dut(descriptionMatches="(?i)video call button").click()
        else:
            dut.shell(
                'am start -a android.intent.action.CALL -d tel:'
                + phone_number
                + ' --ez videocall true'
            )
    elif call_type == 'rtt':
        dut.shell(
            'am start -a android.intent.action.DIAL -d tel:'
            + phone_number
        )
        dut(descriptionMatches="(?i)rtt call button").click()


def call_initiate_gui():
    """Gets call number from UI and starts phone call in Android device"""
    gui_call_type = str(call_type_option)
    gui_call_number = str(call_number_option.get())
    call_initiate(gui_call_type, gui_call_number)


def sys_dump():
    """Opens DumpSys app and displays its main activity on device

    Todo:
        Use Keystring app to open Dumpsys on 'user' devices

    """
    if getprop_check('ro.build.type') == 'user':
        messagebox.showinfo('Error', 'Feature available for [eng] devices only')

    if getprop_check('ro.build.type') == 'eng':
        dut = u2.connect()
        dut.shell('am start -S com.sec.android.app.servicemodeapp/.SysDump')


def ims_logger():
    """Opens IMSLogger app and displays its main activity on devices

    Todo:
        Use Keystring app to open IMS Settings app on 'user' devices
        Navigate IMS Settings app and open IMSLogger

    """
    if getprop_check('ro.build.type') == 'user':
        messagebox.showinfo('Error', 'Feature available for [eng] devices only')

    if getprop_check('ro.build.type') == 'eng':
        dut = u2.connect()
        dut.shell('am start -S com.sec.imslogger/.MainActivity')


def keystring_app():
    """Opens Keystring app and displays its main activity on device"""
    if getprop_check('ro.build.type') == 'user':
        messagebox.showinfo('Error', 'Feature available for [eng] devices only')

    if getprop_check('ro.build.type') == 'eng':
        dut = u2.connect()
        dut.shell('am start -S com.sec.keystringscreen/.MainActivity')


def enable_mobile_data():
    """Enables mobile data on device. Uses broadcast or user interface according to build-type property

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        dut.shell('am start -S com.samsung.android.app.telephonyui/'
                  'com.samsung.android.app.telephonyui.netsettings.ui.NetSettingsActivity')
        dut.wait_activity('.netsettings.ui.NetSettingsActivity')
        switch_2g = dut(className="android.widget.LinearLayout") \
            .child_by_text('Mobile Data', className='android.widget.RelativeLayout') \
            .right(className='android.widget.Switch')
        if not switch_2g.info['checked']:
            switch_2g.click()
        dut.shell('input keyevent KEYCODE_HOME')
    if getprop_check('ro.build.type') == 'eng':
        dut.shell('svc data enable')


def disable_mobile_data():
    """Disables mobile data on device. Uses broadcast or user interface according to build-type property

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        dut.shell('am start -S com.samsung.android.app.telephonyui/'
                  'com.samsung.android.app.telephonyui.netsettings.ui.NetSettingsActivity')
        dut.wait_activity('.netsettings.ui.NetSettingsActivity')
        switch_2g = dut(className="android.widget.LinearLayout") \
            .child_by_text('Mobile Data', className='android.widget.RelativeLayout') \
            .right(className='android.widget.Switch')
        if switch_2g.info['checked']:
            switch_2g.click()
        dut.shell('input keyevent KEYCODE_HOME')
    if getprop_check('ro.build.type') == 'eng':
        dut.shell('svc data disable')


def enable_wifi():  # same as enable_airplane_mode()
    """Enables wifi on device. Uses broadcast or user interface according to build-type property

    Todo:
        Check for airplane mode on 'user' build

    """
    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        dut.shell(r'am start -S com.android.settings/.Settings\$WifiSettingsActivity')
        dut.wait_activity('.Settings$WifiSettingsActivity')
        switch_airplane_mode = dut(className='android.widget.Switch')
        if not switch_airplane_mode.info['checked']:
            switch_airplane_mode.click()
        dut.shell('input keyevent KEYCODE_HOME')
    if getprop_check('ro.build.type') == 'eng':
        dut.shell('svc wifi enable')


def disable_wifi():
    """Disables wifi on device. Uses broadcast or user interface according to build-type property

    Todo:
        Check for airplane mode on 'user' build

    """

    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        dut.shell(r'am start -S com.android.settings/.Settings\$WifiSettingsActivity')
        dut.wait_activity('.Settings$WifiSettingsActivity')
        switch_airplane_mode = dut(className='android.widget.Switch')
        if switch_airplane_mode.info['checked']:
            switch_airplane_mode.click()
        dut.shell('input keyevent KEYCODE_HOME')
    if getprop_check('ro.build.type') == 'eng':
        dut.shell('svc wifi disable')


def enable_roaming():
    """Enables mobile roaming on device. Uses broadcast or user interface according to build-type property

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()

    if getprop_check('ro.build.type') == 'user':
        dut.shell('am start -S com.samsung.android.app.telephonyui/'
                  'com.samsung.android.app.telephonyui.netsettings.ui.NetSettingsActivity')
        dut.wait_activity('.netsettings.ui.NetSettingsActivity')
        switch_2g = dut(className="android.widget.LinearLayout") \
            .child_by_text('International Data Roaming', className='android.widget.RelativeLayout') \
            .right(className='android.widget.Switch')
        if not switch_2g.info['checked']:
            switch_2g.click()
        dut.shell('input keyevent KEYCODE_HOME')
    if getprop_check('ro.build.type') == 'eng':  # does not show confirmation
        dut.shell('settings put global data_roaming 1')


def disable_roaming():
    """Disables mobile roaming on device. Uses broadcast or user interface according to build-type property

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        dut.shell('am start -S com.samsung.android.app.telephonyui/'
                  'com.samsung.android.app.telephonyui.netsettings.ui.NetSettingsActivity')
        dut.wait_activity('.netsettings.ui.NetSettingsActivity')
        switch_2g = dut(className="android.widget.LinearLayout") \
            .child_by_text('International Data Roaming', className='android.widget.RelativeLayout') \
            .right(className='android.widget.Switch')
        if switch_2g.info['checked']:
            switch_2g.click()
        dut.shell('input keyevent KEYCODE_HOME')
    if getprop_check('ro.build.type') == 'eng':  # does not show confirmation
        dut.shell('settings put global data_roaming 0')


def enable_video_call():
    messagebox.showwarning('Warning', 'Feature under development')


def disable_video_call():
    messagebox.showwarning('Warning', 'Feature under development')


def enable_2g():
    """Enables 2G on device via user interface

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()

    dut.shell('am start -S com.samsung.android.app.telephonyui/'
              'com.samsung.android.app.telephonyui.netsettings.ui.NetSettingsActivity')  # works in Android 10
    dut.wait_activity('.netsettings.ui.NetSettingsActivity')
    switch_2g = dut(className="android.widget.LinearLayout") \
        .child_by_text('Allow 2G Service', className='android.widget.RelativeLayout') \
        .right(className='android.widget.Switch')
    if not switch_2g.info['checked']:
        switch_2g.click()
    dut.shell('input keyevent KEYCODE_HOME')


def disable_2g():
    """Disables 2G on device via user interface

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()
    dut.shell('am start -S com.samsung.android.app.telephonyui/'
              'com.samsung.android.app.telephonyui.netsettings.ui.NetSettingsActivity')
    dut.wait_activity('.netsettings.ui.NetSettingsActivity')
    switch_2g = dut(className="android.widget.LinearLayout") \
        .child_by_text('Allow 2G Service', className='android.widget.RelativeLayout') \
        .right(className='android.widget.Switch')
    if switch_2g.info['checked']:
        switch_2g.click()
        if dut(text='Attention').exists(timeout=3):
            dut(text='OK').click()
    dut.shell('input keyevent KEYCODE_HOME')


def enable_rtt():
    """Enables RTT on device via user interface

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()
    dut.shell('am start -S com.samsung.android.app.telephonyui/'
              '.callsettings.ui.preference.CallSettingsActivity')
    dut.wait_activity('.callsettings.ui.preference.CallSettingsActivity')
    rtt_button = dut(text='Real Time Text')
    if rtt_button.exists(timeout=3):
        if rtt_button.info['enabled']:
            rtt_button.click()
            dut(text='RTT call button').click(timeout=3)
            dut(text='Always visible').click(timeout=3)
        else:
            messagebox.showinfo('Error', 'RTT can\'t be enabled\nAirplane mode is enabled on DUT')
    dut.shell('input keyevent KEYCODE_HOME')


def disable_rtt():
    """Disables RTT on device via user interface

    Todo:
        Check for airplane mode
        Check for SIM card presence

    """
    dut = u2.connect()
    dut.shell('am start -S com.samsung.android.app.telephonyui/'
              '.callsettings.ui.preference.CallSettingsActivity')
    dut.wait_activity('.callsettings.ui.preference.CallSettingsActivity')
    rtt_button = dut(text='Real Time Text')
    if rtt_button.exists(timeout=3):
        if rtt_button.info['enabled']:
            rtt_button.click()
            dut(text='RTT call button').click(timeout=3)
            dut(text='Visible during calls').click(timeout=3)
        else:
            messagebox.showinfo('Error', 'RTT can\'t be disabled\nAirplane mode is enabled on DUT')


def disable_animations():
    """Disables animations on 'eng' devices

    Todo:
        Change settings on 'user' devices

    """
    dut = u2.connect()
    if getprop_check('ro.build.type') == 'user':
        messagebox.showinfo('Error', 'Feature available for [eng] devices only')
        # dut.shell('am start -a com.android.settings.APPLICATION_DEVELOPMENT_SETTINGS')
        # dut.wait_activity('.Settings$DevelopmentSettingsDashboardActivity')
    if getprop_check('ro.build.type') == 'eng':
        dut.shell('settings put global window_animation_scale 0')
        dut.shell('settings put global transition_animation_scale 0')
        dut.shell('settings put global animator_duration_scale 0')


def stay_awake():
    """Enables 'stay awake' setting on user interface"""
    if getprop_check('ro.build.type') == 'user':
        dut = u2.connect()
        dut.shell('am start -a com.android.settings.APPLICATION_DEVELOPMENT_SETTINGS')
        dut.wait_activity('.Settings$DevelopmentSettingsDashboardActivity')
        switch_stay_awake = dut(className="android.widget.LinearLayout") \
            .child_by_text('Stay awake', className='android.widget.RelativeLayout') \
            .right(className='android.widget.Switch')
        if not switch_stay_awake.info['checked']:
            switch_stay_awake.click()
        dut.shell('input keyevent KEYCODE_HOME')
    if getprop_check('ro.build.type') == 'eng':
        dut = u2.connect()
        dut.shell('settings put global stay_on_while_plugged_in 3')


def lock_screen():
    """Changes lock screen type to 'None' on device"""
    dut = u2.connect()
    dut.shell('am start -a android.app.action.SET_NEW_PASSWORD')
    dut(text='None').click()


def quick_settings_show():  # works in all binaries - sdk 26+
    """Show 'quick settings' bar on device"""
    dut = u2.connect()
    dut.shell('cmd statusbar expand-settings')


def contacts_clear():
    """Clear data from all 'Contacts' apps"""
    dut = u2.connect()
    dut.shell('pm clear com.sec.android.widgetapp.easymodecontactswidget')
    dut.shell('pm clear com.samsung.android.app.contacts')
    dut.shell('pm clear com.google.android.syncadapters.contacts')
    dut.shell('pm clear com.samsung.android.providers.contacts')
    dut.shell('pm clear com.samsung.android.contacts')


def wake_up():
    """Turns device screen on"""
    dut = u2.connect()
    dut.shell('input keyevent KEYCODE_WAKEUP')


def unlock():
    """Unlocks device screen"""
    dut = u2.connect()
    dut.shell('input keyevent KEYCODE_MENU')


def anritsu_clear():
    """Clears app data from 'Anritsu' app"""
    dut = u2.connect()
    dut.shell('pm clear com.anritsu.APMclient')


def phone_clear():
    """Clear data from all 'Phone' apps"""
    dut = u2.connect()
    dut.shell('pm clear com.android.providers.telephony')
    dut.shell('pm clear com.samsung.android.app.telephonyui')
    dut.shell('pm clear com.sec.phone')
    dut.shell('pm clear com.samsung.android.app.earphonetypec')
    dut.shell('pm clear com.android.phone')


def status_bar_show():
    """Show 'status' bar on device"""
    dut = u2.connect()
    dut.shell('cmd statusbar expand-notifications')


def date_time():
    """Displays date/time activity on device screen"""
    dut = u2.connect()
    dut.shell('am start -a android.settings.DATE_SETTINGS')


def install_uiautomator2():
    """Install uiautomator2 applications on device"""
    subprocess.Popen('uiautomator2 init', creationflags=subprocess.CREATE_NEW_CONSOLE)


def device_info():
    """Displays device CSC, model, AP and build type"""
    sales_code = getprop_check('ro.csc.sales_code')
    model = getprop_check('ro.product.model')
    pda = getprop_check('ro.build.PDA')
    build_type = getprop_check('ro.build.type')

    messagebox.showinfo('Device information',
                        'Device model: ' + model + '\n' +
                        'PDA: ' + pda + '\n' +
                        'CSC: ' + sales_code + '\n' +
                        'Build type: ' + build_type)


# TODO: distribute tabs across files
# TODO: consider switching to OOP model
# FIXME: revamp the "Phone calls" tab, that is plain ugly
# TODO: add voice, video, wifi, rtt call options to "Phone calls" tab
# TODO: add SMS actions
# FIXME: reorder content in "operations" and "settings" tabs
# TODO: change app icon
# TODO: consider implementing a "launch" screen
# TODO: consider adding labels/colors, like
#  "green supports user/eng, blue supports eng only, red is under construction"
# FIXME: create a frame inside each tab, with a fixed size, and adjust the content to this frame

# basic GUI settings

window = tk.Tk()
window.title("Heracles - GUI helper for ATLAS")
#window.tk.call('wm', 'iconphoto', window.w, tk.PhotoImage(file='mobicon.ico'))

# set window as "always on top"

window.wm_attributes('-topmost', 1)

# add tabs

tab_control = ttk.Notebook(window)

# Airplane mode and Reboot tab

airplane_mode_tab = ttk.Label(tab_control)
tab_control.add(airplane_mode_tab, text='Power on/off')
tab_control.pack(expand=1, fill='none')

# Airplane mode, reboot buttons

airplane_mode_on_button = tk.Button(airplane_mode_tab,
                                    text="Enable airplane mode (Power OFF)",
                                    command=airplane_mode_on) \
    .pack(expand=1, fill='both')

airplane_mode_off_button = tk.Button(airplane_mode_tab,
                                     text="Disable airplane mode (Power ON)",
                                     command=airplane_mode_off) \
    .pack(expand=1, fill='both')

reboot_button = tk.Button(airplane_mode_tab,
                          text="Reboot device",
                          command=reboot) \
    .pack(expand=1, fill='both')

# Call Setup tab

phone_calls_tab = ttk.Frame(tab_control)
tab_control.add(phone_calls_tab, text='Phone calls')
tab_control.pack(expand=1, fill='both')

mo_call_labelframe = ttk.Labelframe(phone_calls_tab, text='MO call')
mo_call_labelframe.pack(expand=1, fill='both')
mo_call_labelframe.rowconfigure(0, weight=1)
mo_call_labelframe.columnconfigure(0, weight=1)
mo_call_labelframe.columnconfigure(1, weight=1)

# MO Call radio button settings

radio_frame = ttk.Frame(mo_call_labelframe)
radio_frame.grid(row=0, column=0, sticky='nsew')

call_type_option = tk.StringVar()

voice_call_radiobutton = tk.Radiobutton(radio_frame,
                                        text="Voice Call",
                                        value='voice',
                                        variable=call_type_option)

voice_call_radiobutton.pack(expand=1, fill='both')

video_call_radiobutton = tk.Radiobutton(radio_frame,
                                        text="Video Call",
                                        value='video',
                                        variable=call_type_option)

video_call_radiobutton.pack(expand=1, fill='both')

call_type_option.set('0')

# Phone Number text entry (no validation)

phone_number_labelframe = ttk.Labelframe(mo_call_labelframe, text='Phone number')
phone_number_labelframe.grid(row=0, column=1, sticky='n')

call_number_option = tk.Entry(phone_number_labelframe)
call_number_option.pack(expand=1, fill='both')

# Call button

dial_button = tk.Button(mo_call_labelframe,
                        text="Make call",
                        command=call_initiate_gui) \
    .grid(row=0, column=2, sticky='nsew')

mt_call_labelframe = ttk.Labelframe(phone_calls_tab, text='MT call')
mt_call_labelframe.pack(expand=1, fill='both')
mt_call_labelframe.rowconfigure(0, weight=1)
mt_call_labelframe.columnconfigure(0, weight=1)
mt_call_labelframe.columnconfigure(1, weight=1)

# MT call Answer button

call_answer_button = tk.Button(mt_call_labelframe,
                               text="Answer call",
                               command=call_answer) \
    .grid(row=0, column=0, sticky='nsew')

# MT call End button

call_end_button = tk.Button(mt_call_labelframe,
                            text="End call",
                            command=call_end) \
    .grid(row=0, column=1, sticky='nsew')

# Logging tab

logging_tab = ttk.Frame(tab_control)
tab_control.add(logging_tab, text='Logging')
tab_control.pack(expand=1, fill='both')

sysdump_button = tk.Button(logging_tab,
                           text="Sysdump/Silent log",
                           command=sys_dump) \
    .pack(expand=1, fill='both')

imslogger_button = tk.Button(logging_tab,
                             text="IMS logger",
                             command=ims_logger) \
    .pack(expand=1, fill='both')

keystring_button = tk.Button(logging_tab,
                             text="Launch Keystring app",
                             command=keystring_app) \
    .pack(expand=1, fill='both')

# Quick actions tab

dut_tab = ttk.Frame(tab_control)
tab_control.add(dut_tab, text='Quick actions')
tab_control.pack(expand=1, fill='both')

enable_mobile_data_button = tk.Button(dut_tab,
                                      text="Enable mobile data",
                                      command=enable_mobile_data) \
    .grid(row=0, column=0, sticky='nsew')

disable_mobile_data_button = tk.Button(dut_tab,
                                       text="Disable mobile data",
                                       command=disable_mobile_data) \
    .grid(row=1, column=0, sticky='nsew')

enable_wifi_button = tk.Button(dut_tab,
                               text="Enable WiFi",  # https://www.tourtech.com/2019/01/how-do-you-spell-wifi/
                               command=enable_wifi) \
    .grid(row=2, column=0, sticky='nsew')

disable_wifi_button = tk.Button(dut_tab,
                                text="Disable WiFi",
                                command=disable_wifi) \
    .grid(row=3, column=0, sticky='nsew')

enable_roaming_button = tk.Button(dut_tab,
                                  text="Enable roaming",
                                  command=enable_roaming) \
    .grid(row=0, column=1, sticky='nsew')

disable_roaming_button = tk.Button(dut_tab,
                                   text="Disable roaming",
                                   command=disable_roaming) \
    .grid(row=1, column=1, sticky='nsew')

enable_video_call_button = tk.Button(dut_tab,
                                     text="Enable video call",
                                     command=enable_video_call) \
    .grid(row=2, column=1, sticky='nsew')

disable_video_call_button = tk.Button(dut_tab,
                                      text="Disable video call",
                                      command=disable_video_call) \
    .grid(row=3, column=1, sticky='nsew')

enable_2g_button = tk.Button(dut_tab,
                             text="Enable 2G",
                             command=enable_2g) \
    .grid(row=0, column=2, sticky='nsew')

disable_2g_button = tk.Button(dut_tab,
                              text="Disable 2G",
                              command=disable_2g) \
    .grid(row=1, column=2, sticky='nsew')

enable_rtt_button = tk.Button(dut_tab,
                              text="Enable RTT",
                              command=enable_rtt) \
    .grid(row=2, column=2, sticky='nsew')

disable_rtt_button = tk.Button(dut_tab,
                               text="Disable RTT",
                               command=disable_rtt) \
    .grid(row=3, column=2, sticky='nsew')

# Preconfig tab

settings_tab = ttk.Frame(tab_control)
tab_control.add(settings_tab, text='DUT settings')
tab_control.pack(expand=1, fill='both')

disable_animations_button = tk.Button(settings_tab,
                                      text="Disable animations",
                                      command=disable_animations) \
    .grid(row=0, column=0, sticky='nsew')

stay_awake_button = tk.Button(settings_tab,
                              text="Enable 'Stay Awake'",
                              command=stay_awake) \
    .grid(row=1, column=0, sticky='nsew')

disable_lock_screen_button = tk.Button(settings_tab,
                                       text="Lock screen 'None'",
                                       command=lock_screen) \
    .grid(row=2, column=0, sticky='nsew')

contacts_clear_button = tk.Button(settings_tab,
                                  text="Clear all contacts",
                                  command=contacts_clear) \
    .grid(row=3, column=0, sticky='nsew')

dut_wakeup_button = tk.Button(settings_tab,
                              text="Wake up DUT",
                              command=wake_up) \
    .grid(row=0, column=1, sticky='nsew')

dut_unlock_button = tk.Button(settings_tab,
                              text="Unlock DUT",
                              command=unlock) \
    .grid(row=1, column=1, sticky='nsew')

anritsu_clear_button = tk.Button(settings_tab,
                                 text="Clear Anritsu app",
                                 command=anritsu_clear) \
    .grid(row=2, column=1, sticky='nsew')

phone_clear_button = tk.Button(settings_tab,
                               text="Clear Phone app",
                               command=phone_clear) \
    .grid(row=3, column=1, sticky='nsew')

status_bar_show_button = tk.Button(settings_tab,
                                   text="Show status bar",
                                   command=status_bar_show) \
    .grid(row=0, column=2, sticky='nsew')

date_time_button = tk.Button(settings_tab,
                             text="Date/time settings",
                             command=date_time) \
    .grid(row=1, column=2, sticky='nsew')

uiautomator2_button = tk.Button(settings_tab,
                                text="Install uiautomator2",
                                command=install_uiautomator2) \
    .grid(row=2, column=2, sticky='nsew')

device_info_button = tk.Button(settings_tab,
                               text="Show device info",
                               command=device_info) \
    .grid(row=3, column=2, sticky='nsew')

dut_tab.grid_rowconfigure(0, weight=1)
dut_tab.grid_columnconfigure(0, weight=1)

dut_tab.grid_rowconfigure(1, weight=1)
dut_tab.grid_columnconfigure(1, weight=1)

dut_tab.grid_rowconfigure(2, weight=1)
dut_tab.grid_columnconfigure(2, weight=1)

settings_tab.grid_rowconfigure(0, weight=1)
settings_tab.grid_columnconfigure(0, weight=1)

settings_tab.grid_rowconfigure(1, weight=1)
settings_tab.grid_columnconfigure(1, weight=1)

settings_tab.grid_rowconfigure(2, weight=1)
settings_tab.grid_columnconfigure(2, weight=1)

def main():
    window.mainloop()


if __name__ == "__main__":
    main()
