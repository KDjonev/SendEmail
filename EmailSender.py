#!/usr/bin/python

# Derived from: https://docs.python.org/3.3/library/email-examples.html

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from EmailOptionsParser import EmailOptionsParser
import getpass
import glob
import mimetypes
import os
import smtplib


COMMASPACE = ', '


def SendEmail(
  FromAddress,
  ToAddresses,
  Subject,
  Body,
  Attatchments,
  FromAddressPassword=""):

    Server = smtplib.SMTP('smtp.gmail.com', 587)
    Server.ehlo()
    Server.starttls()
    Server.ehlo()
    NotLoggedIn = True
    while (NotLoggedIn):
        if (FromAddressPassword == ""):
            FromAddressPassword = getpass.getpass(
                'FromAddressPassword for ' + FromAddress + ': ')
        try:
            Server.login(FromAddress.split('@')[0], FromAddressPassword)
        except smtplib.SMTPAuthenticationError:
            print("")
            print("Authentication Error.")
            print("Google is either blocking you're log in attempt,")
            print("or the password was incorrect.")
            print("Feel free to try your password again,")
            print("or check your gmail for an email regarding an"
                  " unauthorized login attempt.")
            FromAddressPassword = ""
            continue
        NotLoggedIn = False

    Message = MIMEMultipart()
    Message['From'] = FromAddress
    Message['To'] = COMMASPACE.join(ToAddresses)
    Message['Subject'] = Subject
    Message.attach(MIMEText(Body, 'plain'))

    # Attatch any necessary files
    if (len(Attatchments) >= 0):
        for File in Attatchments:
            Path, Filename = os.path.split(File)
            if (Path == '' and Filename != ''):
                Path = '.'
            FilePath = os.path.join(Path, Filename)
            if (os.path.isfile(Filename)):
                Attatchment = CreateAttatchment(FilePath)
                Message.attach(Attatchment)
            elif ('*' in FilePath):
                FileList = glob.glob(FilePath)
                for ExpandedFilePath in FileList:
                    Attatchment = CreateAttatchment(ExpandedFilePath)
                    Message.attach(Attatchment)

    MessageText = Message.as_string()
    Server.sendmail(FromAddress, ToAddresses, MessageText)
    Server.quit()


def CreateAttatchment(FilePath):
    if (os.path.isfile(FilePath)):
        # Guess the content type based on the file's extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip'd or compressed files.
        ContentType, Encoding = mimetypes.guess_type(FilePath)
        if ContentType is None or Encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ContentType = 'application/octet-stream'
        Maintype, Subtype = ContentType.split('/', 1)
        if Maintype == 'text':
            FileObject = open(FilePath)
            # Note: we should handle calculating the charset
            Attatchment = MIMEText(FileObject.read(), _subtype=Subtype)
            FileObject.close()
        elif Maintype == 'image':
            FileObject = open(FilePath, 'rb')
            Attatchment = MIMEImage(FileObject.read(), _subtype=Subtype)
            FileObject.close()
        elif Maintype == 'audio':
            FileObject = open(FilePath, 'rb')
            Attatchment = MIMEAudio(FileObject.read(), _subtype=Subtype)
            FileObject.close()
        else:
            FileObject = open(FilePath, 'rb')
            Attatchment = MIMEBase(Maintype, Subtype)
            Attatchment.set_payload(FileObject.read())
            FileObject.close()
            # Encode the payload using Base64
            encoders.encode_base64(Attatchment)
        # Set the filename parameter
        Attatchment.add_header(
            'Content-Disposition',
            'attachment',
            filename=os.path.basename(FilePath))
        return Attatchment


if __name__ == '__main__':

    EmailOptions = EmailOptionsParser()
    EmailOptions.LoadDefaultValues("HaltEmailOptions.eo")
    SendEmail(
        EmailOptions.FromAddress,
        EmailOptions.ToAddresses,
        EmailOptions.Subject,
        EmailOptions.Body,
        EmailOptions.Attatchments,
        EmailOptions.FromAddressPassword)
