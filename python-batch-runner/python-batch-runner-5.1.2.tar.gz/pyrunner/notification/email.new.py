# Copyright 2019 Comcast Cable Communications Management, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import time, smtplib
from datetime import datetime as datetime
from pyrunner.notification.abstract import Notification
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class EmailNotification(Notification):
  
  def emit_notification(self, config, register):
    if not config['email']:
      print('Email address not provided - skipping notification email')
      return 0
    
    failed_objects = register.failed_nodes
    subject, message = '', ''
    attachments = [config.ctllog_file]
    
    # Build message body
    message += "Dear User,\n\n"
    
    if failed_objects:
      message += "{} has failed on {}.\n\n".format(config['app_name'], datetime.now().strftime("%Y-%m-%d"))
      message += "The following tasks have failed:\n"
      for node in failed_objects:
        attachments.append(node.logfile)
        message += "    - {}\n".format(node.name)
      message += "\nPlease refer to the attached logs for more details.\n\n"
      subject = "{} - FAILURE".format(config['app_name'])
    else:
      message += "{} has succeeded on {}.\n\n".format(config['app_name'], datetime.now().strftime("%Y-%m-%d"))
      subject = "{} - SUCCESS".format(config['app_name'])
    
    message += "Execution Details:\n\n"
    
    message += "Start Time: {} {}\n".format(config['app_start_time'], time.strftime("%Z", time.gmtime()))
    message += "End Time: {} {}\n\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), time.strftime("%Z", time.gmtime()))
    
    message += "Log Directory: {}\n\n".format(config['log_dir'])
    
    print('Sending Email Notification to: {}'.format(config['email']))
    command = ['mailx', '-s', subject]
    
    if attachments:
      for a in attachments:
        command.append('-a')
        command.append(a)
    
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Our family reunion'
    msg['From'] = me
    msg['To'] = config['email']
    msg.preamble = message
    
    # Assume we know that the image files are all in PNG format
    for file in pngfiles:
        # Open the files in binary mode.  Let the MIMEImage class automatically
        # guess the specific image type.
        with open(file, 'rb') as fp:
            img = MIMEImage(fp.read())
        msg.attach(img)
    
    # Send the email via our own SMTP server.
    try:
      s = smtplib.SMTP('localhost')
      s.sendmail(me, family, msg.as_string())
      s.quit()
    except ConnectionRefusedError as e:
      print('No SMTP server available for localhost')
      raise
    
    ###################
    command.append(config['email'])
    
    proc = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate(input = str.encode(message))
    retcode = proc.returncode
    
    if retcode > 0:
      if out:
        print(out)
      if err:
        print(err)
      raise RuntimeError('Error while sending notification email')
    
    return retcode