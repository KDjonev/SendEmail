#!/usr/bin/python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import sys


class EmailOptionsParser:

    FromAddress = ''
    FromAddressPassword = ''
    ToAddresses = []
    Subject = ''
    Body = ''
    Attatchments = []

    def LoadDefaultValues(self, DefaultValueFile):
        FileHandler = open(DefaultValueFile).read()
        SoupXmlParser = BeautifulSoup(FileHandler, 'xml')

        EmailOptionsTag = SoupXmlParser.find('EmailOptions')
        if (EmailOptionsTag):
            if (EmailOptionsTag.has_attr('FromAddress')):
                self.FromAddress = EmailOptionsTag['FromAddress']
            if (EmailOptionsTag.has_attr('FromAddressPassword')):
                self.FromAddressPassword = \
                    EmailOptionsTag['FromAddressPassword']
            if (EmailOptionsTag.has_attr('ToAddresses')):
                self.ToAddresses = EmailOptionsTag['ToAddresses'].split(' ')
            if (EmailOptionsTag.has_attr('Subject')):
                self.Subject = EmailOptionsTag['Subject']
            if (EmailOptionsTag.has_attr('Body')):
                self.Body = EmailOptionsTag['Body']
            if (EmailOptionsTag.has_attr('Attatchments')):
                self.Attatchments = EmailOptionsTag['Attatchments'].split(' ')

    def ParseEmailOptionsParserParser(self):

        Parser = ArgumentParser(
            description="Send an e-mail.")

        Parser.add_argument(
            '-f', '--from',
            action='store',
            metavar='FromAddress',
            dest='FromAddress',
            help='The Sender (Required if no default found)')
        Parser.add_argument(
            '-t', '--to',
            nargs='+',
            action='store',
            metavar='ToAddresses',
            dest='ToAddresses',
            help='The Recipient (At least one required if no default found)')
        Parser.add_argument(
            '-s', '--subject',
            action='store',
            metavar='Subject',
            dest='Subject',
            help='The value of the Subject: header')
        Parser.add_argument(
            '-b', '--body',
            action='store',
            metavar='Body',
            dest='Body',
            help='The content of the message body')
        Parser.add_argument(
            '-a', '--attatchments',
            nargs='+',
            action='store',
            metavar='Attatchments',
            dest='Attatchments',
            help='Files that you would like to attatch to the email')

        Options = Parser.parse_args()

        if (not Options.ToAddresses and self.ToAddresses == []):
            Parser.print_help()
            sys.exit(1)
        if (not Options.FromAddress and self.FromAddress == ''):
            Parser.print_help()
            sys.exit(1)

        if (Options.FromAddress):
            self.FromAddress = Options.FromAddress
        if (Options.ToAddresses):
            self.ToAddresses = Options.ToAddresses
        if (Options.Subject):
            self.Subject = Options.Subject
        if (Options.Body):
            self.Body = Options.Body
        if (Options.Attatchments):
            self.Attatchments = Options.Attatchments
