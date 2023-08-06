import os
from dateutil import parser

import pickle
import warnings
import pandas as pd
import numpy as np
import datetime as dt
from time import sleep
import multiprocessing as mp
from threading import Thread
import tempfile
from ftplib import FTP
from logging import log
warnings.filterwarnings('ignore')

class WalkFTP:
    
    def list_path(self, x):
        try:
            return self._ftp.nlst(x)
        except:
            sleep(60)
            self.connect_ftp()
            return self._ftp.nlst(x)
        
    def check_in_log(self, f, stat_mtime):
        '''
        return True if run ftp download
        '''
        log = self.log_data
        if log == {}: 
            return True
        
        log_file_entry = log.get(f, {})
        if log_file_entry == {}:
            self.class_print('log empty for {} - glob ftp. Running Normal'.format(f))
            return True
        else:
            
            # check if successful get
            if log_file_entry.get('get', False):
                # successful get
                
                if log_file_entry.get('mtime') == stat_mtime:
                    # successful mtim
                    
                    if callable(self.processing_function):
                        # is a process
                        if log_file_entry.get('process', False):
                            self.class_print('Not pulling {} - it is in the log'.format(f))
                            return False
                        else:
                            self.class_print('pulling {} - did not process correctly'.format(f))
                            return True
                            
                    else:
                        self.class_print('Not pulling {} - it is in the log'.format(f))
                        return False
                            
                    
                else:
                    self.class_print('mtime does not match for {} log: {} current: {}'.format(
                        f, log_file_entry.get('mtime'), stat_mtime
                    ))
                    return True
                    
                
            else:
                self.class_print('ftp get did not work {}'.format(f))
                return True
            
        
    def glob_ftp(self, store_paths = ''):
        
        if self._glob_count > self.args.get('break_count', np.inf): 
            return None
        
        for new_fp_or_file in self.list_path(store_paths):
            
            #new_fp_or_file = os.path.join(store_paths, f)
            stat_bool, stat_mtime = self.test_file(new_fp_or_file)
            
            if stat_bool:
                stat_mtime = str(stat_mtime)
                date_filter = (pd.to_datetime(stat_mtime) >= pd.to_datetime(self.start_date)) and (pd.to_datetime(stat_mtime) <= pd.to_datetime(self.end_date) )
                
                
                if date_filter and self.check_in_log(new_fp_or_file, stat_mtime):
                    self.class_print('{} {} {}'.format(stat_mtime, new_fp_or_file, date_filter))
                    self._glob_count+=1
                    self.q.put(new_fp_or_file)
                else:
                    pass
                    self.class_print(f'{new_fp_or_file} date_filter: {date_filter} stat_mtime: {stat_mtime}')
                    
                if self._glob_count > self.args.get('break_count', np.inf):
                    self.class_print('publishing glob break')
                    self.q.put('break')
                    return None
                
                
            else:
                self.class_print(f'STAT BOOL FALSE {new_fp_or_file}')
                block = False
                for b in self.blocks:
                    if b in new_fp_or_file:
                        block=True
                        break
                        
                if not block:
                    self.glob_ftp(new_fp_or_file)
                    
        if store_paths == self.orig_store_paths:
            self.class_print('publishing glob break')
            self.q.put('break')
    
    def test_file(self, f):
        try:
            nlist = self._ftp.nlst(f)
        except:
            return False, None
            
        if nlist == [] or nlist[0]==f:
            mtime = self.extract_modified_time(f)
            return True, mtime
        else:
            #self.class_print(f'{f} {nlist}')
            return False, None
    
    def store_all_ftp(self):
        break_count = self.args.get('break_count',np.inf)
        count=0
        while True:
            
            fp = self.q.get()
            
            if isinstance(fp, str) and fp == 'break' or (count>break_count):
                self.class_print('publishing process break')
                self.process_q.put(('break', 'break'))
                break
                
            elif fp is None:
                sleep(1)
            
            elif isinstance(fp, str):
                count+=1
                self.class_print('storing: {}'.format(fp))
                self.store_ftp(fp)
                
                
            self.class_print('.........')
            
            
        self.class_print('finished get function')
        
    def store_ftp(self, fp):
        
        store_path = os.path.join(self._output_path, os.path.dirname(fp))
        store_file = os.path.join(self._output_path, fp)

        if not os.path.exists(store_path):
            os.makedirs(store_path)
        
        if not os.path.exists(store_file):
            try:
                self.get(fp, store_file)
            except Exception as e:
                print('ERROR ON: {} {}'.format(fp, store_file))
                print(e)
                            
    def exit_q(self):
        self.process_q.put(('break', 'break'))
        self.q.put('break')
        self.cleanup()
        
    def connect_ftp(self, returns=False):
        ftp = FTP(self._base_url)
        max_try_count = 2
        count = 0
        while count<max_try_count:
            count+=1
            try:
                if not returns: self.class_print('logging into ftp')
                if self._username is None and self._password is None:
                    mg = ftp.login(user=self._username, passwd=self._password)
                    if not returns: self.class_print(msg)
                else:
                    msg = ftp.login(user=self._username, passwd=self._password)
                    if not returns: self.class_print(msg)
                
                break
            except:
                sleep(30)
                
                
        if returns:
            return ftp
        else:
            self._ftp = ftp
                
    def cleanup(self):
        self._ftp.close()
        
        if self.close_temporary_directory:
            self.tmpdir.cleanup()
    
    def extract_modified_time(self, remotepath):
        
        ftp = self.connect_ftp(returns=True)
        ts = None
        try:
            ts = ftp.voidcmd('MDTM '+remotepath)
            ts = ts[4:].strip()
            ts = parser.parse(ts)
            ts = pd.to_datetime(ts)
            return ts
        
        #    return ts
        except Exception as e:
            self.class_print(f'{remotepath} {e}')
            return ''
            assert False, f'{ts} {remotepath}'
        #    if '.' in remotepath:
        #        print(e)
        #    return None
    
    
    def get(self, remotepath, file):
        count=0
        successful_get = False
        ftp = self._ftp
        start_time = pd.datetime.now()
        
        for i in range(0,2):
            
            #self.connect_ftp()
            self.class_print(f'starting store get {remotepath}')
            
            try:
                
                stat_mtime = self.extract_modified_time(remotepath)
                
                gFile = open(file, 'wb')
                self.class_print('reading: {}'.format(remotepath))
                ftp.retrbinary('RETR '+remotepath, gFile.write, blocksize=self._blocksize)               
                
                self.class_print(f'finished _s get {remotepath}')
                successful_get=True
                self.add_log(remotepath,'get',successful_get)
                self.add_log(remotepath,'mtime', stat_mtime)
                #self.add_log(remotepath, 'stat', stat)
                break
                
            except Exception as e: 
                self.class_print(remotepath)
                self.class_print(e)
                self.connect_ftp()
                ftp = self._ftp
        
        if count > 0: ftp.close()
        if not successful_get and os.path.exists(file): os.remove(file)
        assert successful_get, '{} failed'.format(file)
        self.class_print('successful ftp pull {} seconds'.format( int((pd.datetime.now()-start_time).total_seconds()) ))
        
        if callable(self.processing_function): 
            self.process_q.put((file, remotepath))
            
    def class_print(self, msg):
        if self.print_out:
            print(pd.datetime.today().strftime('%Y-%m-%d %H:%M:%S')+' '+str(msg))
            
    
    def main(self):
        
        self.q = mp.Queue()
        self.process_q = mp.Queue()
        
        self.connect_ftp()
        
        glob_thread = Thread(target=self.glob_ftp, name = 'glob')
        glob_thread.start()
        
        store_thread = Thread(target=self.store_all_ftp, name='store')
        store_thread.start()
        
        if callable(self.processing_function): 
            process_thread = Thread(target=self.process_all_ftp, name='process')
            process_thread.start()
        
        
        while True:
            if self.join_threads:
                self.class_print('joining glob thread')
                glob_thread.join()
                self.class_print('joining store thread')
                store_thread.join()
                
                if callable(self.processing_function): 
                    self.class_print('joining process thread')
                    process_thread.join()
                    
                break
                
            #self.class_print('END ---- did not join threads ')
        
    def process_all_ftp(self):
        break_count = self.args.get('break_count',np.inf)
        count=0
        
        while True:
            
            
            fname = self.process_q.get()
            self.class_print('process all ftp finished get {}'.format(fname))
            
            if fname is None:
                self.class_print('SLEEPING')
                sleep(1)
                
                
            elif isinstance(fname[0], str) and fname[0] != 'break':
                count+=1
                successful_process = self.processing_function(fname[0])
                self.add_log(fname[1], 'process', successful_process)
                self.class_print(f'process count is {count}')
                
            elif (isinstance(fname[0], str) and fname[0] == 'break') or (count>break_count):
                self.class_print('JOINING THREADS')
                self.join_threads = True
                return None
                
                
    
    def write_log(self):
        fp = self.log
        if not os.path.exists(os.path.dirname(fp)):
            os.makedirs(os.path.dirname(fp))
            
        if ready: self.log_data['_ready'] = True
        pickle.dump(self.log_data, open(self.log, mode='wb'))
    
    def add_log(self, fp, key, value):
        if not fp in self.log_data:
            self.log_data[fp] = {}
        
        self.log_data[fp][key] = value
    
    
    def read_log(self):
        if self.log is None:
            self.log_data = {}
            
        elif os.path.exists(self.log):
            first = True
            while True:
                
                self.log_data = pickle.load(open(self.log, mode='rb'))
                
                if self._force or self.log_data.get('_ready', True):
                    
                    # this section prevents other FTPs from downloading while this one is running so your log is not double written
                    self.log_data['_ready'] = False
                    self.write_log()
                    break
                else:
                    if first: 
                        first = False
                        self.class_print('sleeping ftp in process of running')
                    sleep(60)
                    
            
            
        else:
            self.log_data = {}
    
        self.class_print('finished reading log')
        
    
    
    def __init__(
        self, 
        base_url, 
        username=None,
        password=None,
        port=21,
        store=None, 
        processing_function=None,
        log=None,
        blocks=[],
        start_date = pd.to_datetime('1970-01-01'),
        end_date = pd.datetime.today()+dt.timedelta(1),
        blocksize=8192,
        **args,
    ):
        '''
        Parameters
        ----------
        base_url : str
            URL that you are pulling the ftp
        username : str
            Username to login to the ftp
        password : str
            Username to login to the ftp
        port : int
            port
        store : None, str
            Path after to store files. If None, then 
            stores in a temporary directory. Use with
            1) processing_function argument to get 
            data from them and a log filepath to keep
            track of files already downloaded
        processing_function : None/function
            pass function if you want to process the 
            data after ftp pull. Takes teh filepath as an
            argument. Returns True/False depending on whether
            the process ran correctly
        log : str
            filepath of log to get information on data.
            This can be used for a temporary directory
            in order to not keep the files stored but 
            know that the data is processed. Should be
            a .p file
        blocks : list
            list of str to block. Looks for string
            in file path of each entry in blocks
            to determine whether to pull
        start_date : str/datetime
            date to only pull files that were modified after
            this date - default 1970-01-01
            
        Optional Args
        -------------
        print_out : bool
            Whether to print out messages (slower when True)
        break_count : int
            stop running ftp download after n number of files downloaded
        force : bool
            force to overwrite log that is in progress
        '''
        self.args=args
        self._glob_count=0
        print_out = args.get('print_out', False)
        self._force = args.get('force', False)
        
        if isinstance(blocks, str):
            blocks = [blocks]
            
        self.blocks = blocks
        self.print_out = print_out
        
        if not store is None:
            self.class_print(f'store is not None: {store}')
            self._output_path = store
            self.close_temporary_directory = False
        else:
            self.close_temporary_directory = True
            self.tmpdir = tempfile.TemporaryDirectory()
            self._output_path = self.tmpdir.name
            self.class_print(f'temporary directory {self._output_path}')
            
        self._blocksize = blocksize
        self.log = log
        self.read_log()
        self.join_threads = False
        
        self._username = username
        self._password = password
        self._port=port
        self._base_url = base_url
        self.processing_function = processing_function
        self.file_list = []
        self.orig_store_paths = ''
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.run()
        if log != None: self.write_log(ready=True)
        
    def run(self):
        self.main()
        self.cleanup()