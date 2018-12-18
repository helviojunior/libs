#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import socket
import sys
import os, re, sys, queue, time, datetime, threading, json

class Logger(object):
    ''' Helper object for easily printing colored text to the terminal. '''

    out_file = ''

    @staticmethod
    def pl(text, Console=True):
        '''Prints text using colored format with trailing new line.'''
        if Console:
            Color.pl(text)

        if Logger.out_file != '':
            try:
                with open(Logger.out_file, "a") as text_file:
                    text_file.write(Color.sc(text) + '\n')
            except:
                pass

class Configuration(object):
    ''' Stores configuration variables and functions for Turbo Search. '''
    version = '0.0.9'

    domain = ''
    word_list = ''
    out_file = ''
    tasks = 5
    verbose =False
    cmd_line = ''

    @staticmethod
    def load_from_arguments():
        ''' Sets configuration values based on Argument.args object '''
        import getopt, argparse


        parser = argparse.ArgumentParser()

        requiredNamed = parser.add_argument_group('SETTINGS')

        requiredNamed.add_argument('-d',
            action='store',
            dest='dns_sufix',
            metavar='[dns sufix]',
            type=str,
            required=True,
            help=Color.s('Sufix to DNS check (ex: {G}helviojunior.com.br{W})'))

        requiredNamed.add_argument('-w',
            action='store',
            dest='word_list',
            metavar='[word list]',
            type=str,
            default='',
            required=True,
            help='Word list to be tested')

        customNamed = parser.add_argument_group('CUSTOM')


        customNamed.add_argument('-t',
            action='store',
            dest='tasks',
            default=5,
            metavar='[tasks]',
            type=int,
            help=Color.s('Number of threads in parallel (default: {G}5{W})'))

        customNamed.add_argument('-o',
            action='store',
            dest='out_file',
            metavar='[output file]',
            type=str,
            help=Color.s('save output to disk (default: {G}none{W})'))

        args = parser.parse_args()

        for a in sys.argv:
            Configuration.cmd_line += "%s " % a

        Configuration.domain = args.dns_sufix
        Configuration.word_list = args.word_list

        if args.tasks:
            Configuration.tasks = args.tasks

        if Configuration.tasks < 1:
            Configuration.tasks = 1

        if Configuration.tasks > 256:
            Configuration.tasks = 256

        if args.out_file:
            Configuration.out_file = args.out_file
            Logger.out_file = Configuration.out_file

        config_check = 0
        if Configuration.word_list == '':
            config_check = 1

        if config_check == 1:
            Configuration.mandatory()


        Logger.pl(Configuration.cmd_line, False)
        Logger.pl(' ', False)


        Logger.pl('{+} {W}Startup parameters')


        if not os.path.isfile(Configuration.word_list):
            Color.pl('{!} {R}error: word list file not found {O}%s{R}{W}\r\n' % Configuration.word_list)
            Configuration.exit_gracefully(0)

        try:
            with open(Configuration.word_list, 'r') as f:
                # file opened for writing. write to it here
                pass
        except IOError as x:
            if x.errno == errno.EACCES:
                Logger.pl('{!} {R}error: could not open word list file {O}permission denied{R}{W}\r\n')
                sys.exit(0)
            elif x.errno == errno.EISDIR:
                Logger.pl('{!} {R}error: could not open word list file {O}it is an directory{R}{W}\r\n')
                sys.exit(0)
            else:
                Logger.pl('{!} {R}error: could not open word list file {W}\r\n')
                sys.exit(0)

        Logger.pl('     {C}word list:{O} %s{W}' % Configuration.word_list)
        Logger.pl('     {C}dns sufix:{O} %s{W}' % Configuration.domain)
        Logger.pl('     {C}tasks:{O} %s{W}' % Configuration.tasks)

    @staticmethod
    def mandatory():
        Color.pl('{!} {R}error: missing a mandatory option ({O}-d and -w{R}){G}, use -h help{W}\r\n')
        sys.exit(0)

class Color(object):
    ''' Helper object for easily printing colored text to the terminal. '''

    # Basic console colors
    colors = {
        'W' : '\033[0m',  # white (normal)
        'R' : '\033[31m', # red
        'G' : '\033[32m', # green
        'O' : '\033[33m', # orange
        'B' : '\033[34m', # blue
        'P' : '\033[35m', # purple
        'C' : '\033[36m', # cyan
        'GR': '\033[37m', # gray
        'D' : '\033[2m'   # dims current color. {W} resets.
    }

    # Helper string replacements
    replacements = {
        '{+}': ' {W}{D}[{W}{G}+{W}{D}]{W}',
        '{!}': ' {O}[{R}!{O}]{W}',
        '{?}': ' {W}[{C}?{W}]',
        '{*}': ' {W}[{B}*{W}]'
    }

    last_sameline_length = 0

    @staticmethod
    def p(text):
        '''
        Prints text using colored format on same line.
        Example:
            Color.p("{R}This text is red. {W} This text is white")
        '''
        sys.stdout.write(Color.s(text))
        sys.stdout.flush()
        if '\r' in text:
            text = text[text.rfind('\r')+1:]
            Color.last_sameline_length = len(text)
        else:
            Color.last_sameline_length += len(text)

    @staticmethod
    def pl(text):
        '''Prints text using colored format with trailing new line.'''
        Color.p('%s\n' % text)
        Color.last_sameline_length = 0

    @staticmethod
    def pe(text):
        '''Prints text using colored format with leading and trailing new line to STDERR.'''
        sys.stderr.write(Color.s('%s\n' % text))
        Color.last_sameline_length = 0

    @staticmethod
    def s(text):
        ''' Returns colored string '''
        output = text
        for (key,value) in Color.replacements.items():
            output = output.replace(key, value)
        for (key,value) in Color.colors.items():
            output = output.replace("{%s}" % key, value)
        return output

    @staticmethod
    def sc(text):
        ''' Returns non colored string '''
        output = text
        for (key,value) in Color.replacements.items():
            output = output.replace(key, value)
        for (key,value) in Color.colors.items():
            output = output.replace("{%s}" % key, '')
        return output

    @staticmethod
    def clear_line():
        spaces = ' ' * Color.last_sameline_length
        sys.stdout.write('\r%s\r' % spaces)
        sys.stdout.flush()
        Color.last_sameline_length = 0

    @staticmethod
    def clear_entire_line():
        import os
        (rows, columns) = os.popen('stty size', 'r').read().split()
        Color.p("\r" + (" " * int(columns)) + "\r")



class DNSGetter:

    words = []
    q = queue.Queue()
    added = []
    last = {}
    last_start = []
    ingnored =0
    listed = []


    def __init__(self):
        pass

    def load_wordlist(self):
        self.words = []
        insert = True
        
        if os.path.isfile("enumdns.restore"):
            try:
                with open("enumdns.restore", 'r') as f:
                    dt = json.load(f)
                    for i in dt["threads"]:
                        self.last_start.append(dt["threads"][i].replace(".%s" % Configuration.domain, ""))

            except Exception as e:
                raise   

        if len(self.last_start) > 0:
            insert = False

        with open(Configuration.word_list, 'r', encoding="ascii", errors="surrogateescape") as f:
            try:
                line = f.readline()
                line = line.lower()

                while line:
                    if line.endswith('\n'):
                        line = line[:-1]
                    if line.endswith('\r'):
                        line = line[:-1]

                    line = ''.join(filter(self.permited_char, line))

                    if not insert and line in self.last_start:
                        insert = True                        

                    if insert:
                        self.words.append(line.strip())
                    else:
                        self.ingnored += 1

                    try:
                        line = f.readline()
                    except:
                        pass
            except KeyboardInterrupt:
                raise
            except:
                raise

    def len(self):
        return len(self.words)


    def permited_char(self, s):
        if s.isalpha():
            return True
        elif bool(re.match("^[A-Za-z0-9_-]*$", s)):
            return True
        elif s == ".":
            return True
        else:
            return False



    def run(self):

        t = threading.Thread(target=self.worker, kwargs=dict(index=-1))
        t.daemon = True
        t.start()

        #if len(self.words) < Configuration.tasks:
        #    Configuration.tasks = 1

        self.do_work(Configuration.domain)

        t_status = threading.Thread(target=self.status_worker)
        t_status.daemon = True
        t_status.start()

        for i in range(Configuration.tasks):
            self.last[i] = ''
            t = threading.Thread(target=self.worker, kwargs=dict(index=i))
            t.daemon = True
            t.start()

        for item in self.words:
            if item.strip() != '':
                self.q.put("%s.%s" % (item, Configuration.domain))

        self.q.join()  # block until all tasks are done
        sys.stdout.write("\033[K")  # Clear to the end of line

    def status_worker(self):
        try:
            while True:
                try:
                    dt = { "threads": self.last }

                    with open("enumdns.restore", "w") as text_file:
                        text_file.write(json.dumps(dt))
                except:
                    pass
                time.sleep(10)
        except KeyboardInterrupt:
            pass

    def worker(self, index):
        try:
            while True:
                item = self.q.get()
                if index >= 0:
                    self.last[index] = item
                self.do_work(item)
                self.q.task_done()
        except KeyboardInterrupt:
            pass

    def do_work(self, queue_item):
        try:
            sys.stdout.write("\033[K")  # Clear to the end of line
            print(("Testing: %s" % queue_item), end='\r', flush=True)

            ip=socket.gethostbyname(queue_item)
            l='%s : %s'% (queue_item, ip)

            if l not in self.listed:
                self.listed.append(l)
                Logger.pl('{*} {W}%s'% l)

        except:
            pass



class QueueItem:

    url = ''
    dir_not_found = 404

    def __init__(self, url, dir_not_found):
        self.url = url
        self.dir_not_found = dir_not_found

class EnumDNS(object):

    def main(self):
        self.run()

    def run(self):
        try:
            get = DNSGetter()
            get.load_wordlist()

            now = time.time()
            ts = int(now)
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            Logger.pl('     {C}start time {O}%s{W}' % timestamp)
            Logger.pl('     {C}generated {O}%d{C} words{W}' % get.len())
            Logger.pl('     {C}ignored {O}%d{C} words{W}' % get.ingnored)
            Logger.pl(' ')

            Logger.pl('{+} {W}Scanning hosts on DNS sufix {C}%s{W} ' % Configuration.domain)
            get.run()
            Logger.pl('     ')

            if os.path.exists("enumdns.restore"): 
                os.remove("enumdns.restore")

        except Exception as e:
            Color.pl("\n{!} {R}Error: {O}%s" % str(e))
            if Configuration.verbose > 0 or True:
                Color.pl('\n{!} {O}Full stack trace below')
                from traceback import format_exc
                Color.p('\n{!}    ')
                err = format_exc().strip()
                err = err.replace('\n', '\n{W}{!} {W}   ')
                err = err.replace('  File', '{W}{D}File')
                err = err.replace('  Exception: ', '{R}Exception: {O}')
                Color.pl(err)
        except KeyboardInterrupt:
            Color.pl('\n{!} {O}interrupted{W}\n')


        now = time.time()
        ts = int(now)
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        Logger.pl('{+} {C}End time {O}%s{W}' % timestamp)


        Logger.pl("{+} Finished tests against {C}%s{W}, exiting" % Configuration.domain)

        #Configuration.delete_temp()

    def print_banner(self):
        """ Displays ASCII art of the highest caliber.  """
        #Color.pl(Configuration.get_banner())


def run():
    d = EnumDNS()
    d.print_banner()

    Configuration.load_from_arguments()

    if not os.path.isfile(Configuration.word_list):
        Color.pl('\n{!} {R}Error:{O} Wordlist file not found %s{W}' % Configuration.word_list)
        sys .exit(1)

    try:

        d.main()

    except Exception as e:
        Color.pl('\n{!} {R}Error:{O} %s{W}' % str(e))

        if Configuration.verbose > 0 or True:
            Color.pl('\n{!} {O}Full stack trace below')
            from traceback import format_exc
            Color.p('\n{!}    ')
            err = format_exc().strip()
            err = err.replace('\n', '\n{W}{!} {W}   ')
            err = err.replace('  File', '{W}{D}File')
            err = err.replace('  Exception: ', '{R}Exception: {O}')
            Color.pl(err)

        Color.pl('\n{!} {R}Exiting{W}\n')

    except KeyboardInterrupt:
        Color.pl('\n{!} {O}interrupted, shutting down...{W}')

    sys.exit(0)

if __name__ == '__main__':
    run()
