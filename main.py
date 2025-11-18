import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import requests
import vlc
import json
import os
import sys
import socket
from urllib.parse import urlparse, urlencode
import re
import time
import base64
import pickle
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import subprocess
import platform
import threading
from PIL import Image, ImageTk
import io
import concurrent.futures
from datetime import datetime, timedelta

class LoginWindow:
    def __init__(self):
        # إنشاء نافذة الدخول الرئيسية
        self.root = tk.Tk()
        self.root.title("👑 تسجيل الدخول - نوفا الذهبي 👑")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.configure(bg='#1a1a1a')
        
        # مركزة النافذة في منتصف الشاشة
        self.center_window()
        
        # إعدادات النافذة
        self.root.attributes('-topmost', True)  # جعل النافذة في المقدمة
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.result = None
        
        # محاولة تحميل بيانات الدخول المحفوظة
        self.saved_credentials = self.load_saved_credentials()
        self.setup_ui()
    
    def load_saved_credentials(self):
        """تحميل بيانات الدخول المحفوظة"""
        try:
            config_file = "iptv_config.dat"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config_data = json.load(f)
                
                # فك التشفير
                fernet = Fernet(base64.urlsafe_b64encode(b'advanced_iptv_player_extreme_pro_2024_key!'.ljust(32)[:32]))
                
                username = fernet.decrypt(base64.urlsafe_b64decode(config_data['username'])).decode()
                password = fernet.decrypt(base64.urlsafe_b64decode(config_data['password'])).decode()
                
                return {
                    'username': username,
                    'password': password,
                    'auto_save': config_data.get('auto_save', True)
                }
        except Exception as e:
            pass
        return None
    
    def center_window(self):
        """مركزة النافذة في منتصف الشاشة"""
        self.root.update_idletasks()
        width = 450
        height = 400
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # إطار رئيسي
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # شعار التطبيق
        logo_frame = tk.Frame(main_frame, bg='#1a1a1a')
        logo_frame.pack(pady=(0, 30))
        
        tk.Label(logo_frame, text="👑", 
                font=('Arial', 28), 
                fg='#d4af37', bg='#1a1a1a').pack()
        
        tk.Label(logo_frame, text="نوفا الذهبي", 
                font=('Arial', 20, 'bold'), 
                fg='#d4af37', bg='#1a1a1a').pack()
        
        tk.Label(logo_frame, text="سيرفر IPTV المتميز", 
                font=('Arial', 12), 
                fg='#ffffff', bg='#1a1a1a').pack(pady=(5, 0))
        
        # إطار الحقول
        form_frame = tk.Frame(main_frame, bg='#1a1a1a')
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # اسم المستخدم
        user_frame = tk.Frame(form_frame, bg='#1a1a1a')
        user_frame.pack(fill=tk.X, pady=(10, 20))
        
        tk.Label(user_frame, text="👤 اسم المستخدم:", 
                font=('Arial', 11, 'bold'), 
                fg='#ffffff', bg='#1a1a1a', 
                anchor='w').pack(fill='x', pady=(0, 8))
        
        self.username_entry = tk.Entry(user_frame, 
                                     font=('Arial', 12),
                                     bg='#2d2d2d', 
                                     fg='#ffffff',
                                     insertbackground='#ffffff',
                                     relief='flat',
                                     width=30)
        self.username_entry.pack(fill='x', pady=(0, 5), ipady=8)
        
        # كلمة المرور
        pass_frame = tk.Frame(form_frame, bg='#1a1a1a')
        pass_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(pass_frame, text="🔐 كلمة المرور:", 
                font=('Arial', 11, 'bold'), 
                fg='#ffffff', bg='#1a1a1a', 
                anchor='w').pack(fill='x', pady=(0, 8))
        
        self.password_entry = tk.Entry(pass_frame, 
                                     font=('Arial', 12),
                                     bg='#2d2d2d', 
                                     fg='#ffffff',
                                     insertbackground='#ffffff',
                                     show='*',
                                     relief='flat',
                                     width=30)
        self.password_entry.pack(fill='x', pady=(0, 5), ipady=8)
        
        # خيار حفظ البيانات
        self.save_var = tk.BooleanVar(value=True)
        save_frame = tk.Frame(form_frame, bg='#1a1a1a')
        save_frame.pack(fill=tk.X, pady=15)
        
        save_check = tk.Checkbutton(save_frame, 
                                  text="💾 حفظ بيانات الدخول",
                                  variable=self.save_var,
                                  font=('Arial', 10),
                                  fg='#ffffff',
                                  bg='#1a1a1a',
                                  selectcolor='#2d2d2d',
                                  activebackground='#1a1a1a',
                                  activeforeground='#ffffff')
        save_check.pack(anchor='w')
        
        # زر التحميل التلقائي إذا كانت هناك بيانات محفوظة
        if self.saved_credentials:
            auto_load_frame = tk.Frame(form_frame, bg='#1a1a1a')
            auto_load_frame.pack(fill=tk.X, pady=10)
            
            auto_load_btn = tk.Button(auto_load_frame,
                                    text="🔄 استخدام البيانات المحفوظة",
                                    font=('Arial', 10, 'bold'),
                                    bg='#4CAF50',
                                    fg='#ffffff',
                                    activebackground='#45a049',
                                    activeforeground='#ffffff',
                                    relief='flat',
                                    padx=20,
                                    pady=8,
                                    command=self.use_saved_credentials)
            auto_load_btn.pack(fill='x')
            
            # تعبئة الحقول تلقائياً
            self.username_entry.insert(0, self.saved_credentials['username'])
            self.password_entry.insert(0, self.saved_credentials['password'])
            self.save_var.set(self.saved_credentials['auto_save'])
        
        # أزرار التحكم
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # زر الاتصال
        connect_btn = tk.Button(button_frame,
                              text="🚀 اتصال بالسيرفر",
                              font=('Arial', 12, 'bold'),
                              bg='#d4af37',
                              fg='#1a1a1a',
                              activebackground='#ffd700',
                              activeforeground='#1a1a1a',
                              relief='flat',
                              padx=30,
                              pady=12,
                              command=self.connect)
        connect_btn.pack(fill='x', pady=(0, 10))
        
        # زر الإلغاء
        cancel_btn = tk.Button(button_frame,
                             text="خروج",
                             font=('Arial', 11),
                             bg='#5a5a5a',
                             fg='#ffffff',
                             activebackground='#7a7a7a',
                             activeforeground='#ffffff',
                             relief='flat',
                             padx=30,
                             pady=10,
                             command=self.cancel)
        cancel_btn.pack(fill='x')
        
        # ربط زر Enter بالاتصال
        self.root.bind('<Return>', lambda e: self.connect())
        self.root.bind('<Escape>', lambda e: self.cancel())
        
        # تركيز المؤشر على حقل كلمة المرور إذا كانت البيانات محملة
        if not self.saved_credentials:
            self.username_entry.focus()
        else:
            self.password_entry.focus()
        
        # تأثيرات مرئية
        self.setup_visual_effects()
    
    def use_saved_credentials(self):
        """استخدام البيانات المحفوظة تلقائياً"""
        if self.saved_credentials:
            self.username_entry.delete(0, tk.END)
            self.username_entry.insert(0, self.saved_credentials['username'])
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, self.saved_credentials['password'])
            self.save_var.set(self.saved_credentials['auto_save'])
    
    def setup_visual_effects(self):
        """إضافة تأثيرات مرئية للنافذة"""
        # تغيير لون الزر عند المرور بالفأرة
        def on_enter_connect(e):
            e.widget.config(bg='#ffd700')
        
        def on_leave_connect(e):
            e.widget.config(bg='#d4af37')
        
        def on_enter_cancel(e):
            e.widget.config(bg='#7a7a7a')
        
        def on_leave_cancel(e):
            e.widget.config(bg='#5a5a5a')
        
        def on_enter_auto_load(e):
            e.widget.config(bg='#45a049')
        
        def on_leave_auto_load(e):
            e.widget.config(bg='#4CAF50')
        
        # تطبيق التأثيرات على الأزرار
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for btn in child.winfo_children():
                            if isinstance(btn, tk.Button):
                                if "اتصال" in btn.cget('text'):
                                    btn.bind("<Enter>", on_enter_connect)
                                    btn.bind("<Leave>", on_leave_connect)
                                elif "استخدام البيانات" in btn.cget('text'):
                                    btn.bind("<Enter>", on_enter_auto_load)
                                    btn.bind("<Leave>", on_leave_auto_load)
                                else:
                                    btn.bind("<Enter>", on_enter_cancel)
                                    btn.bind("<Leave>", on_leave_cancel)
    
    def connect(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username:
            messagebox.showwarning("تحذير", "يرجى إدخال اسم المستخدم")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showwarning("تحذير", "يرجى إدخال كلمة المرور")
            self.password_entry.focus()
            return
        
        # حفظ البيانات إذا طلب المستخدم ذلك
        if self.save_var.get():
            self.save_credentials(username, password)
        
        # عرض تحميل
        self.show_loading()
        
        # محاكاة التحقق من البيانات
        self.root.after(1500, lambda: self.finish_connection(username, password))
    
    def save_credentials(self, username, password):
        """حفظ بيانات الدخول"""
        try:
            config_file = "iptv_config.dat"
            fernet = Fernet(base64.urlsafe_b64encode(b'advanced_iptv_player_extreme_pro_2024_key!'.ljust(32)[:32]))
            
            config_data = {
                'username': base64.urlsafe_b64encode(fernet.encrypt(username.encode())).decode(),
                'password': base64.urlsafe_b64encode(fernet.encrypt(password.encode())).decode(),
                'auto_save': self.save_var.get(),
                'timestamp': time.time()
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f)
                
        except Exception as e:
            pass
    
    def show_loading(self):
        """عرض شاشة تحميل"""
        for widget in self.root.winfo_children():
            widget.pack_forget()
        
        loading_frame = tk.Frame(self.root, bg='#1a1a1a')
        loading_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(loading_frame, text="👑", 
                font=('Arial', 24), 
                fg='#d4af37', bg='#1a1a1a').pack(pady=(50, 10))
        
        tk.Label(loading_frame, text="جاري الاتصال بالسيرفر...", 
                font=('Arial', 14), 
                fg='#ffffff', bg='#1a1a1a').pack(pady=10)
        
        # محاكاة شريط التقدم
        progress_frame = tk.Frame(loading_frame, bg='#1a1a1a')
        progress_frame.pack(pady=20)
        
        self.progress_var = tk.IntVar()
        progress_bar = ttk.Progressbar(progress_frame, 
                                     variable=self.progress_var,
                                     maximum=100,
                                     length=200,
                                     mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start(10)
    
    def finish_connection(self, username, password):
        """إنهاء عملية الاتصال"""
        self.result = {
            'username': username,
            'password': password,
            'save_credentials': self.save_var.get(),
            'success': True
        }
        self.root.quit()
        self.root.destroy()
    
    def cancel(self):
        self.result = None
        self.root.quit()
        self.root.destroy()
    
    def on_closing(self):
        """عند محاولة إغلاق النافذة"""
        if messagebox.askokcancel("خروج", "هل تريد الخروج من التطبيق؟"):
            self.result = None
            self.root.quit()
            self.root.destroy()
    
    def show(self):
        """عرض نافذة الدخول والانتظار للنتيجة"""
        self.root.mainloop()
        return self.result

class AdvancedIPTVPlayer:
    def __init__(self, root, login_result):
        self.root = root
        self.root.title("👑 اى بى تى فى سيرفر نوفا الاصلى - النسخة الذهبية المتميزة 👑")
        self.root.geometry("1600x900")
        
        # مركزة النافذة الرئيسية
        self.center_main_window()
        
        # إعدادات التحميل
        self.download_queue = []
        self.downloading = False
        self.download_thread = None
        self.download_progress = {}
        self.downloaded_content = {
            'live': {},
            'movies': {},
            'series': {}
        }
        
        # إعدادات التسجيل
        self.recording = False
        self.recording_start_time = None
        self.recording_file = None
        self.recordings_dir = "recordings"
        self.recording_qualities = {
            "عالية (1080p)": "1920x1080",
            "متوسطة (720p)": "1280x720", 
            "قياسية (480p)": "854x480",
            "منخفضة (360p)": "640x360"
        }
        
        # إعدادات الجودة
        self.video_qualities = {
            "أفضل جودة تلقائية": "auto",
            "فائقة الدقة (4K)": "3840x2160",
            "عالية (1080p)": "1920x1080",
            "متوسطة (720p)": "1280x720",
            "قاعدة (480p)": "854x480",
            "منخفضة (360p)": "640x360"
        }
        self.current_quality = "auto"
        
        # مجلدات التحميل
        self.download_folders = {
            'live': "downloads/live",
            'movies': "downloads/movies", 
            'series': "downloads/series",
            'recordings': self.recordings_dir
        }
        
        # إنشاء مجلدات التحميل
        for folder in self.download_folders.values():
            if not os.path.exists(folder):
                os.makedirs(folder)
        
        # التحقق من تثبيت VLC وإصداره بدون رسائل
        self.check_vlc_installation()
        
        # تطبيق الثيم الذهبي المتميز
        self.setup_golden_theme()
        
        # مفتاح التشفير الثابت
        self.encryption_key = b'advanced_iptv_player_extreme_pro_2024_key!'
        
        # بيانات السيرفر مع الهوست الثابت المخفي
        self.server_config = {
            'host': 'tv.nv2.info',
            'port': '80',
            'username': '',
            'password': '',
            'type': 'xtream'
        }
        
        # إعدادات الكاش
        self.cache_enabled = True
        self.cache_duration = 3600
        self.cache_dir = "iptv_cache"
        self.backup_streams = []
        
        # إعدادات الحفظ التلقائي
        self.auto_save_credentials = True
        self.config_file = "iptv_config.dat"
        
        # إنشاء مجلد الكاش
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
        # جلسة requests مع إعدادات محسنة
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'identity',
            'Connection': 'keep-alive'
        })
        
        # إنشاء مشغل VLC مع إعدادات متقدمة حديثة
        self.setup_advanced_vlc_player()
        
        # متغيرات التحكم
        self.channels = []
        self.movies = []
        self.series_categories = []
        self.series = []
        self.series_episodes = []
        self.current_content_index = -1
        self.categories = []
        self.movies_categories = []
        self.current_content_type = "live"
        self.is_player_fullscreen = False
        self.show_channel_info = False
        self.current_series_id = None
        self.content_history = []
        self.current_media_url = None
        self.is_playing_before_fullscreen = False
        self.current_playback_time = 0
        self.show_username = False
        self.server_status = "offline"
        self.retry_count = 0
        self.max_retries = 3
        self.volume_var = tk.IntVar(value=80)
        self.vlc_version = "Unknown"
        
        # صور المحتوى
        self.content_images = {}
        self.image_cache_dir = "image_cache"
        if not os.path.exists(self.image_cache_dir):
            os.makedirs(self.image_cache_dir)
        
        # واجهة المستخدم
        self.create_widgets()
        
        # تحميل البيانات المحفوظة تلقائياً
        self.load_saved_credentials()
        
        # تحميل المحتوى المحلي
        self.load_downloaded_content()
        
        # استخدام بيانات الدخول من نافذة الدخول
        if login_result and login_result.get('success'):
            self.process_login_result(login_result)
        else:
            # إذا لم تكن هناك نتيجة دخول، حاول الاتصال التلقائي بالبيانات المحفوظة
            self.auto_connect_with_saved_credentials()
        
        # بدء مراقبة حالة السيرفر
        self.root.after(5000, self.monitor_server_status)

    def auto_connect_with_saved_credentials(self):
        """الاتصال التلقائي باستخدام البيانات المحفوظة"""
        if hasattr(self, 'user_entry') and self.user_entry.get() and self.pass_entry.get():
            self.root.after(2000, self.connect_server)

    def center_main_window(self):
        """مركزة النافذة الرئيسية في نصف الشاشة"""
        self.root.update_idletasks()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # جعل النافذة بحجم 80% من الشاشة
        width = int(screen_width * 0.8)
        height = int(screen_height * 0.8)
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def process_login_result(self, login_result):
        """معالجة نتيجة الدخول"""
        username = login_result['username']
        password = login_result['password']
        
        # حفظ بيانات الدخول في الواجهة
        self.user_entry.delete(0, tk.END)
        self.user_entry.insert(0, username)
        self.pass_entry.delete(0, tk.END)
        self.pass_entry.insert(0, password)
        
        self.auto_save_credentials = login_result['save_credentials']
        self.save_var.set(self.auto_save_credentials)
        
        # محاولة الاتصال التلقائي
        self.root.after(1000, self.connect_server)

    def check_vlc_installation(self):
        """التحقق من تثبيت VLC وإصداره بدون رسائل مزعجة"""
        try:
            if sys.platform.startswith('win'):
                result = subprocess.run(['vlc', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version_info = result.stdout.strip()
                    self.vlc_version = version_info.split()[0] if version_info else 'إصدار حديث'
            elif sys.platform.startswith('linux'):
                result = subprocess.run(['vlc', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version_info = result.stdout.strip()
                    self.vlc_version = version_info.split()[0] if version_info else 'إصدار حديث'
            elif sys.platform.startswith('darwin'):
                result = subprocess.run(['/Applications/VLC.app/Contents/MacOS/VLC', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version_info = result.stdout.strip()
                    self.vlc_version = version_info.split()[0] if version_info else 'إصدار حديث'
        except Exception as e:
            self.vlc_version = "غير معروف"

    def setup_advanced_vlc_player(self):
        """إعداد مشغل VLC متقدم مع دعم جميع الصيغ الحديثة"""
        try:
            vlc_args = [
                '--no-xlib',
                '--quiet',
                '--network-caching=5000',
                '--file-caching=5000',
                '--live-caching=4000',
                '--codec=avcodec',
                '--avcodec-hw=any',
                '--avcodec-threads=4',
                '--adaptive-logic=rate',
                '--clock-jitter=0',
                '--clock-synchro=0',
                '--drop-late-frames',
                '--skip-frames',
                '--avi-index=10',
                '--avformat-format=mp4,ts,avi,mkv,flv,webm,mov',
                '--demux=avformat',
                '--h264-fps=60',
                '--deinterlace=1',
                '--deinterlace-mode=blend',
                '--audio-resampler=soxr',
                '--audio-channels=2',
                '--sout-mux-caching=2000',
                '--rtsp-tcp',
                '--http-reconnect',
                '--http-continuous',
                '--no-video-title-show',
                '--no-stats',
                '--no-osd',
                '--no-snapshot-preview',
                '--no-interact',
                '--no-loop',
                '--no-video-on-top',
                '--no-embedded-video',
                '--no-keyboard-events',
                '--no-mouse-events',
                '--disable-screensaver',
            ]
            
            self.instance = vlc.Instance(*vlc_args)
            self.media_player = self.instance.media_player_new()
            
            self.vlc_version = self.instance.libvlc_get_version()
            
        except Exception as e:
            # استخدام الطريقة العادية إذا فشلت الطريقة المتقدمة
            try:
                self.instance = vlc.Instance()
                self.media_player = self.instance.media_player_new()
            except:
                # لا نعرض أي رسائل خطأ
                pass

    def setup_golden_theme(self):
        """إعداد ثيم ذهبي متميز بألوان ذهبية وأنيقة"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # الألوان الأساسية للثيم الذهبي
        self.gold_colors = {
            'primary': '#d4af37',
            'secondary': '#ffd700', 
            'dark_bg': '#1a1a1a',
            'medium_bg': '#2d2d2d',
            'light_bg': '#3a3a3a',
            'text_primary': '#ffffff',
            'text_secondary': '#d4af37',
            'accent': '#ffd700',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336'
        }
        
        style.configure(".", 
                       background=self.gold_colors['dark_bg'],
                       foreground=self.gold_colors['text_primary'],
                       fieldbackground=self.gold_colors['medium_bg'],
                       selectbackground=self.gold_colors['primary'],
                       selectforeground=self.gold_colors['dark_bg'],
                       troughcolor=self.gold_colors['light_bg'])
        
        style.configure("Custom.TFrame", background=self.gold_colors['dark_bg'])
        style.configure("Custom.TLabel", background=self.gold_colors['dark_bg'], 
                       foreground=self.gold_colors['text_primary'], font=('Arial', 9))
        style.configure("Title.TLabel", background=self.gold_colors['dark_bg'], 
                       foreground=self.gold_colors['primary'], font=('Arial', 12, 'bold'))
        style.configure("Success.TLabel", background=self.gold_colors['dark_bg'], 
                       foreground=self.gold_colors['success'], font=('Arial', 9, 'bold'))
        style.configure("Warning.TLabel", background=self.gold_colors['dark_bg'], 
                       foreground=self.gold_colors['warning'], font=('Arial', 9, 'bold'))
        style.configure("Error.TLabel", background=self.gold_colors['dark_bg'], 
                       foreground=self.gold_colors['error'], font=('Arial', 9, 'bold'))
        
        style.configure("Golden.TButton",
                       background=self.gold_colors['primary'],
                       foreground=self.gold_colors['dark_bg'],
                       focuscolor=self.gold_colors['secondary'],
                       borderwidth=2,
                       relief="raised",
                       font=('Arial', 9, 'bold'),
                       padding=(10, 5))
        
        style.map("Golden.TButton",
                 background=[('active', self.gold_colors['secondary']), 
                           ('pressed', self.gold_colors['primary']), 
                           ('disabled', '#5a5a5a')],
                 foreground=[('active', self.gold_colors['dark_bg']), 
                           ('pressed', self.gold_colors['dark_bg']), 
                           ('disabled', '#aaaaaa')],
                 relief=[('pressed', 'sunken')])
        
        style.configure("Golden.TEntry", 
                       fieldbackground=self.gold_colors['medium_bg'], 
                       foreground=self.gold_colors['text_primary'], 
                       insertcolor=self.gold_colors['primary'])
        style.configure("Golden.TCombobox", 
                       fieldbackground=self.gold_colors['medium_bg'], 
                       foreground=self.gold_colors['text_primary'])
        
        self.root.configure(bg=self.gold_colors['dark_bg'])

    def create_widgets(self):
        # الإطار الرئيسي
        main_container = ttk.Frame(self.root, style="Custom.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # شريط القوائم المنسدلة
        self.create_menu_bar()
        
        # إطار الإعدادات
        self.settings_frame = ttk.LabelFrame(main_container, text="⚙️ إعدادات السيرفر", padding=10, style="Custom.TFrame")
        self.settings_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # حقول الإدخال
        input_frame = ttk.Frame(self.settings_frame, style="Custom.TFrame")
        input_frame.pack(fill=tk.X)
        
        user_frame = ttk.Frame(input_frame, style="Custom.TFrame")
        user_frame.grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(user_frame, text="👤 المستخدم:", style="Custom.TLabel").pack(side=tk.LEFT)
        self.user_entry = ttk.Entry(user_frame, width=18, font=('Arial', 10), show="*", style="Golden.TEntry")
        self.user_entry.pack(side=tk.LEFT, padx=2)
        
        self.show_user_btn = ttk.Button(user_frame, text="👁️", width=3, style="Golden.TButton",
                                      command=self.toggle_username_visibility)
        self.show_user_btn.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(input_frame, text="🔐 كلمة المرور:", style="Custom.TLabel").grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        self.pass_entry = ttk.Entry(input_frame, width=20, show="*", font=('Arial', 10), style="Golden.TEntry")
        self.pass_entry.grid(row=0, column=2, padx=5, pady=2)
        
        self.save_var = tk.BooleanVar(value=True)
        self.save_check = ttk.Checkbutton(input_frame, text="💾 حفظ البيانات", 
                                         variable=self.save_var,
                                         command=self.toggle_auto_save,
                                         style="Custom.TLabel")
        self.save_check.grid(row=0, column=3, padx=10, pady=2)
        
        # أزرار التحكم الرئيسية
        btn_frame = ttk.Frame(self.settings_frame, style="Custom.TFrame")
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="🔗 اتصال", style="Golden.TButton", command=self.connect_server).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="🔄 إعادة الاتصال", style="Golden.TButton", command=self.reconnect_server).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="🔓 تسجيل دخول جديد", style="Golden.TButton", command=self.show_login_window).pack(side=tk.LEFT, padx=3)
        ttk.Button(btn_frame, text="🗑️ مسح البيانات المحفوظة", style="Golden.TButton", command=self.clear_saved_credentials).pack(side=tk.LEFT, padx=3)
        
        # حالة الاتصال والسيرفر
        status_frame = ttk.Frame(self.settings_frame, style="Custom.TFrame")
        status_frame.pack(fill=tk.X, pady=2)
        
        self.connection_status = ttk.Label(status_frame, text="❌ غير متصل", style="Error.TLabel")
        self.connection_status.pack(side=tk.LEFT, padx=5)
        self.server_status_label = ttk.Label(status_frame, text="🔴 السيرفر غير متاح", style="Error.TLabel")
        self.server_status_label.pack(side=tk.LEFT, padx=5)
        self.cache_status = ttk.Label(status_frame, text="💾 الكاش مفعل", style="Success.TLabel")
        self.cache_status.pack(side=tk.LEFT, padx=5)
        self.download_status = ttk.Label(status_frame, text="💾 جاهز للتحميل", style="Success.TLabel")
        self.download_status.pack(side=tk.LEFT, padx=5)
        self.recording_status = ttk.Label(status_frame, text="⏺️ جاهز للتسجيل", style="Success.TLabel")
        self.recording_status.pack(side=tk.LEFT, padx=5)
        self.save_status = ttk.Label(status_frame, text="💾 الحفظ مفعل", style="Success.TLabel")
        self.save_status.pack(side=tk.LEFT, padx=5)
        
        # معلومات VLC
        self.vlc_info = ttk.Label(status_frame, text=f"VLC: {self.vlc_version.split()[0] if self.vlc_version != 'Unknown' else 'Unknown'}", 
                                 style="Custom.TLabel", foreground=self.gold_colors['primary'])
        self.vlc_info.pack(side=tk.RIGHT, padx=5)
        
        # شريط المسار
        self.path_label = ttk.Label(self.settings_frame, text="المسار: الرئيسية", style="Title.TLabel")
        self.path_label.pack(pady=2)
        
        # الإطار الرئيسي
        self.main_frame = ttk.Frame(main_container, style="Custom.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # إطار القوائم والتصنيفات (مكبر)
        self.left_frame = ttk.Frame(self.main_frame, style="Custom.TFrame", width=500)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # التصنيفات (مكبرة)
        self.cat_frame = ttk.LabelFrame(self.left_frame, text="📂 تصنيفات البث المباشر", padding=8, style="Custom.TFrame")
        self.cat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.cat_listbox = tk.Listbox(self.cat_frame, height=8, font=('Arial', 11), 
                                     bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'], 
                                     selectbackground=self.gold_colors['primary'],
                                     selectforeground=self.gold_colors['dark_bg'], activestyle='none',
                                     highlightcolor=self.gold_colors['primary'],
                                     highlightbackground=self.gold_colors['primary'])
        self.cat_listbox.pack(fill=tk.BOTH, expand=True)
        self.cat_listbox.bind('<<ListboxSelect>>', self.on_category_select)
        
        self.series_cat_frame = ttk.LabelFrame(self.left_frame, text="📂 تصنيفات المسلسلات", padding=8, style="Custom.TFrame")
        self.series_cat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.series_cat_listbox = tk.Listbox(self.series_cat_frame, height=8, font=('Arial', 11),
                                           bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'],
                                           selectbackground=self.gold_colors['primary'],
                                           selectforeground=self.gold_colors['dark_bg'], activestyle='none',
                                           highlightcolor=self.gold_colors['primary'])
        self.series_cat_listbox.pack(fill=tk.BOTH, expand=True)
        self.series_cat_listbox.bind('<<ListboxSelect>>', self.on_series_category_select)
        
        self.movies_cat_frame = ttk.LabelFrame(self.left_frame, text="📂 تصنيفات الأفلام", padding=8, style="Custom.TFrame")
        self.movies_cat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        self.movies_cat_listbox = tk.Listbox(self.movies_cat_frame, height=8, font=('Arial', 11),
                                           bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'],
                                           selectbackground=self.gold_colors['primary'],
                                           selectforeground=self.gold_colors['dark_bg'], activestyle='none',
                                           highlightcolor=self.gold_colors['primary'])
        self.movies_cat_listbox.pack(fill=tk.BOTH, expand=True)
        self.movies_cat_listbox.bind('<<ListboxSelect>>', self.on_movies_category_select)
        
        # المحتوى مع الصور (مكبر)
        self.content_frame = ttk.LabelFrame(self.left_frame, text="📺 البث المباشر (0)", padding=8, style="Custom.TFrame")
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # شريط البحث
        search_frame = ttk.Frame(self.content_frame, style="Custom.TFrame")
        search_frame.pack(fill=tk.X, pady=5)
        ttk.Label(search_frame, text="🔍 بحث:", style="Custom.TLabel").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 11), style="Golden.TEntry")
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        search_entry.bind('<KeyRelease>', self.search_content)
        
        # إنشاء Listbox مع دعم الصور (مكبر)
        self.content_listbox = tk.Listbox(self.content_frame, font=('Arial', 12),
                                        bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'],
                                        selectbackground=self.gold_colors['primary'],
                                        selectforeground=self.gold_colors['dark_bg'], activestyle='none',
                                        highlightcolor=self.gold_colors['primary'])
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.content_listbox.yview)
        self.content_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.content_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.content_listbox.bind('<Double-Button-1>', self.on_content_double_click)
        self.content_listbox.bind('<<ListboxSelect>>', self.on_content_select)
        
        # إطار الفيديو (مكبر)
        self.video_frame = ttk.LabelFrame(self.main_frame, text="👑 المشغل الذهبي المتميز", padding=8, style="Custom.TFrame")
        self.video_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.video_panel = tk.Frame(self.video_frame, bg='#000000', relief='sunken', bd=2)
        self.video_panel.pack(fill=tk.BOTH, expand=True)
        
        # معلومات القناة مع الصورة
        self.info_frame = ttk.Frame(self.video_frame, style="Custom.TFrame")
        self.info_frame.pack(fill=tk.X, pady=5)
        
        self.info_image_label = ttk.Label(self.info_frame, style="Custom.TLabel")
        self.info_image_label.pack()
        
        self.info_label = ttk.Label(self.info_frame, text="🔒 المعلومات مخفية", style="Title.TLabel")
        self.info_label.pack()
        self.stream_info = ttk.Label(self.info_frame, text="", style="Custom.TLabel", foreground=self.gold_colors['primary'])
        self.stream_info.pack()
        
        # شريط التقدم
        self.progress_frame = ttk.Frame(self.video_frame, style="Custom.TFrame")
        self.progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(self.progress_frame, text="00:00 / 00:00", style="Custom.TLabel")
        self.progress_label.pack()
        
        self.progress_var = tk.DoubleVar()
        self.progress_scale = ttk.Scale(self.progress_frame, from_=0, to=100, variable=self.progress_var, 
                                      command=self.seek_video, orient=tk.HORIZONTAL, style="Custom.Horizontal.TScale")
        self.progress_scale.pack(fill=tk.X, padx=5)
        
        # شريط التحكم
        self.control_bar = ttk.Frame(main_container, style="Custom.TFrame")
        self.control_bar.pack(fill=tk.X, padx=10, pady=5)
        self.create_control_bar()
        
        # إخفاء إطارات التصنيفات في البداية
        self.hide_all_category_frames()
        
        # بدء تحديث التقدم
        self.update_progress()
        
        # تعيين نافذة VLC الأولية
        self.root.after(100, self.set_vlc_window)
        
        # ربط حدث مفتاح Escape للخروج من ملء الشاشة
        self.root.bind('<Escape>', lambda e: self.exit_player_fullscreen())

    def show_login_window(self):
        """عرض نافذة دخول جديدة"""
        # إخفاء النافذة الرئيسية مؤقتاً
        self.root.withdraw()
        
        # إنشاء نافذة الدخول
        login = LoginWindow()
        result = login.show()
        
        # إعادة إظهار النافذة الرئيسية
        self.root.deiconify()
        
        if result and result.get('success'):
            self.process_login_result(result)

    def create_menu_bar(self):
        """إنشاء شريط القوائم المنسدلة"""
        menubar = tk.Menu(self.root, bg=self.gold_colors['dark_bg'], fg=self.gold_colors['text_primary'])
        self.root.config(menu=menubar)
        
        # قائمة المحتوى
        content_menu = tk.Menu(menubar, tearoff=0, bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'])
        menubar.add_cascade(label="📡 المحتوى", menu=content_menu)
        content_menu.add_command(label="📡 بث مباشر", command=lambda: self.load_content("live"))
        content_menu.add_command(label="🎬 أفلام", command=lambda: self.load_content("movies"))
        content_menu.add_command(label="📺 مسلسلات", command=lambda: self.load_content("series"))
        content_menu.add_separator()
        content_menu.add_command(label="💾 المحتوى المحلي", command=self.show_downloaded_content)
        
        # قائمة الجودة والتسجيل
        quality_menu = tk.Menu(menubar, tearoff=0, bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'])
        menubar.add_cascade(label="🎚️ الجودة والتسجيل", menu=quality_menu)
        
        # الجودة
        quality_submenu = tk.Menu(quality_menu, tearoff=0, bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'])
        quality_menu.add_cascade(label="🎚️ جودة التشغيل", menu=quality_submenu)
        for quality in self.video_qualities.keys():
            quality_submenu.add_command(label=quality, command=lambda q=quality: self.set_quality(q))
        
        # التسجيل
        record_submenu = tk.Menu(quality_menu, tearoff=0, bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'])
        quality_menu.add_cascade(label="⏺️ التسجيل", menu=record_submenu)
        record_submenu.add_command(label="⏺️ بدء/إيقاف التسجيل", command=self.toggle_recording)
        record_submenu.add_command(label="📁 فتح مجلد التسجيلات", command=self.open_recordings_folder)
        
        # قائمة التحميل
        download_menu = tk.Menu(menubar, tearoff=0, bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'])
        menubar.add_cascade(label="⬇️ التحميل", menu=download_menu)
        download_menu.add_command(label="⬇️ تحميل المحدد", command=self.download_selected)
        download_menu.add_command(label="🖼️ تحميل الصور", command=self.download_all_images)
        
        # قائمة العرض
        view_menu = tk.Menu(menubar, tearoff=0, bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'])
        menubar.add_cascade(label="👁️ العرض", menu=view_menu)
        view_menu.add_command(label="👁️ إظهار/إخفاء المعلومات", command=self.toggle_channel_info)
        view_menu.add_command(label="⛶ ملء شاشة المشغل", command=self.toggle_player_fullscreen)
        view_menu.add_separator()
        view_menu.add_command(label="📋 العودة", command=self.go_back)
        view_menu.add_command(label="🏠 الرئيسية", command=self.go_home)
        
        # قائمة الإعدادات
        settings_menu = tk.Menu(menubar, tearoff=0, bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'])
        menubar.add_cascade(label="⚙️ الإعدادات", menu=settings_menu)
        settings_menu.add_command(label="🎛️ إعدادات VLC", command=self.show_vlc_settings)
        settings_menu.add_command(label="💾 تفعيل/تعطيل الكاش", command=self.toggle_cache)
        settings_menu.add_command(label="🗑️ مسح الكاش", command=self.clear_cache)
        settings_menu.add_command(label="📊 حالة السيرفر", command=self.check_server_status)
        settings_menu.add_separator()
        settings_menu.add_command(label="🔓 إظهار اليوزر المخزن", command=self.show_saved_username)
        settings_menu.add_command(label="🔄 تحديث المحتوى", command=self.refresh_content)
        settings_menu.add_separator()
        settings_menu.add_command(label="🔓 تسجيل دخول جديد", command=self.show_login_window)
        settings_menu.add_command(label="🗑️ مسح البيانات المحفوظة", command=self.clear_saved_credentials)

    def create_control_bar(self):
        """إنشاء شريط تحكم محسن"""
        control_frame = ttk.Frame(self.control_bar, style="Custom.TFrame")
        control_frame.pack(fill=tk.X)
        
        ttk.Button(control_frame, text="⏸️ إيقاف", style="Golden.TButton", command=self.pause_video).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="▶️ تشغيل", style="Golden.TButton", command=self.play_video_current).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏹️ إيقاف", style="Golden.TButton", command=self.stop_video).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔊 صوت", style="Golden.TButton", command=self.toggle_mute).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔈 -", style="Golden.TButton", command=self.volume_down).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔊 +", style="Golden.TButton", command=self.volume_up).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏪ 10s", style="Golden.TButton", command=lambda: self.seek_relative(-10)).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏩ 10s", style="Golden.TButton", command=lambda: self.seek_relative(10)).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏮️ سابق", style="Golden.TButton", command=self.previous_content).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="⏭️ تالي", style="Golden.TButton", command=self.next_content).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🔄 إعادة تشغيل", style="Golden.TButton", command=self.restart_video).pack(side=tk.LEFT, padx=2)
        
        # شريط الصوت
        ttk.Label(control_frame, text="🔊:", style="Custom.TLabel").pack(side=tk.LEFT, padx=2)
        volume_scale = ttk.Scale(control_frame, from_=0, to=100, variable=self.volume_var, 
                                command=self.set_volume, orient=tk.HORIZONTAL, length=80, style="Custom.Horizontal.TScale")
        volume_scale.pack(side=tk.LEFT, padx=2)
        
        # اختيار الجودة
        ttk.Label(control_frame, text="🎚️ جودة:", style="Custom.TLabel").pack(side=tk.LEFT, padx=2)
        self.quality_var = tk.StringVar(value="أفضل جودة تلقائية")
        quality_combo = ttk.Combobox(control_frame, textvariable=self.quality_var, 
                                   values=list(self.video_qualities.keys()), 
                                   state="readonly", style="Golden.TCombobox", width=20)
        quality_combo.pack(side=tk.LEFT, padx=2)
        quality_combo.bind('<<ComboboxSelected>>', self.on_quality_change)
        
        # زر التسجيل
        self.record_btn = ttk.Button(control_frame, text="⏺️ بدء التسجيل", style="Golden.TButton", command=self.toggle_recording)
        self.record_btn.pack(side=tk.LEFT, padx=5)
        
        # حالة التشغيل
        self.play_status = ttk.Label(control_frame, text="⏹️ متوقف", style="Custom.TLabel")
        self.play_status.pack(side=tk.RIGHT, padx=10)

    def set_quality(self, quality):
        """تعيين جودة التشغيل من القائمة"""
        self.quality_var.set(quality)
        self.on_quality_change()

    def on_quality_change(self, event=None):
        """تغيير جودة التشغيل"""
        selected_quality = self.quality_var.get()
        self.current_quality = self.video_qualities.get(selected_quality, "auto")
        
        # إذا كان هناك فيديو قيد التشغيل، إعادة تشغيله بالجودة الجديدة
        if self.media_player.is_playing() and self.current_media_url:
            self.restart_video_with_quality()

    def restart_video_with_quality(self):
        """إعادة تشغيل الفيديو بالجودة المحددة"""
        try:
            current_time = self.media_player.get_time()
            was_playing = self.media_player.is_playing()
            
            self.media_player.stop()
            
            # إعادة التشغيل مع الجودة الجديدة
            content_item = self.get_current_content_item()
            if content_item:
                title = content_item.get('name', 'محتوى')
                self.play_video_advanced(self.current_media_url, title)
                
                # استعادة الوقت إذا كان ذلك ممكناً
                if was_playing and current_time > 0:
                    self.root.after(2000, lambda: self.media_player.set_time(current_time))
                    
        except Exception as e:
            pass

    def toggle_recording(self):
        """تبديل حالة التسجيل"""
        if not self.media_player.is_playing():
            messagebox.showwarning("تحذير", "لا يوجد بث قيد التشغيل للتسجيل")
            return
        
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        """بدء التسجيل"""
        try:
            content_item = self.get_current_content_item()
            if not content_item:
                messagebox.showerror("خطأ", "لا يوجد محتوى محدد للتسجيل")
                return
            
            content_name = content_item.get('name', 'تسجيل')
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{self.sanitize_filename(content_name)}_{timestamp}.mp4"
            filepath = os.path.join(self.recordings_dir, filename)
            
            # إنشاء مجلد التسجيلات إذا لم يكن موجوداً
            if not os.path.exists(self.recordings_dir):
                os.makedirs(self.recordings_dir)
            
            # بدء التسجيل باستخدام VLC
            media = self.media_player.get_media()
            if media:
                # إعدادات التسجيل
                record_options = [
                    f'sout=#duplicate{{dst=display,dst=std{{access=file,mux=mp4,dst="{filepath}"}}}}',
                    'sout-keep'
                ]
                
                for option in record_options:
                    media.add_option(option)
                
                self.media_player.set_media(media)
                self.media_player.play()
                
                self.recording = True
                self.recording_start_time = time.time()
                self.recording_file = filepath
                
                self.record_btn.config(text="⏹️ إيقاف التسجيل")
                self.recording_status.config(text="🔴 تسجيل قيد التشغيل", style="Error.TLabel")
                
                messagebox.showinfo("بدء التسجيل", f"بدأ التسجيل: {content_name}")
                
                # بدء تحديث وقت التسجيل
                self.update_recording_time()
                
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر بدء التسجيل: {str(e)}")

    def stop_recording(self):
        """إيقاف التسجيل"""
        try:
            if self.recording:
                # إيقاف التسجيل عن طريق إعادة تشغيل الوسائط بدون خيارات التسجيل
                current_time = self.media_player.get_time()
                was_playing = self.media_player.is_playing()
                
                self.media_player.stop()
                
                # إعادة التشغيل بدون تسجيل
                if self.current_media_url:
                    content_item = self.get_current_content_item()
                    if content_item:
                        title = content_item.get('name', 'محتوى')
                        self.play_video_advanced(self.current_media_url, title)
                        
                        # استعادة الوقت إذا كان ذلك ممكناً
                        if was_playing and current_time > 0:
                            self.root.after(2000, lambda: self.media_player.set_time(current_time))
                
                recording_duration = time.time() - self.recording_start_time
                file_size = os.path.getsize(self.recording_file) if os.path.exists(self.recording_file) else 0
                
                self.recording = False
                self.recording_start_time = None
                
                self.record_btn.config(text="⏺️ بدء التسجيل")
                self.recording_status.config(text="⏺️ جاهز للتسجيل", style="Success.TLabel")
                
                messagebox.showinfo("إيقاف التسجيل", 
                                  f"تم إيقاف التسجيل\n"
                                  f"المدة: {self.format_time(recording_duration)}\n"
                                  f"حجم الملف: {file_size // (1024*1024)} MB\n"
                                  f"المسار: {self.recording_file}")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر إيقاف التسجيل: {str(e)}")

    def update_recording_time(self):
        """تحديث وقت التسجيل"""
        if self.recording:
            elapsed_time = time.time() - self.recording_start_time
            self.recording_status.config(
                text=f"🔴 تسجيل: {self.format_time(elapsed_time)}", 
                style="Error.TLabel"
            )
            self.root.after(1000, self.update_recording_time)

    def open_recordings_folder(self):
        """فتح مجلد التسجيلات"""
        try:
            if not os.path.exists(self.recordings_dir):
                os.makedirs(self.recordings_dir)
            
            if sys.platform.startswith('win'):
                os.startfile(self.recordings_dir)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', self.recordings_dir])
            else:
                subprocess.Popen(['xdg-open', self.recordings_dir])
                
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر فتح مجلد التسجيلات: {str(e)}")

    def download_content_image(self, content_item, content_type):
        """تحميل صورة المحتوى"""
        try:
            stream_icon = content_item.get('stream_icon') or content_item.get('cover') or content_item.get('movie_image')
            if not stream_icon:
                return None
                
            image_key = hashlib.md5(stream_icon.encode()).hexdigest()
            cache_path = os.path.join(self.image_cache_dir, f"{image_key}.jpg")
            
            # التحقق من وجود الصورة في الكاش
            if os.path.exists(cache_path):
                return cache_path
            
            # تحميل الصورة
            response = self.session.get(stream_icon, timeout=10, verify=False)
            if response.status_code == 200:
                with open(cache_path, 'wb') as f:
                    f.write(response.content)
                return cache_path
                
        except Exception as e:
            pass
            
        return None

    def download_all_images(self):
        """تحميل جميع صور المحتوى"""
        def download_thread():
            self.download_status.config(text="🔄 جاري تحميل الصور...", style="Warning.TLabel")
            
            all_content = []
            if self.current_content_type == "live":
                all_content = self.channels
            elif self.current_content_type == "movies":
                all_content = self.movies
            elif self.current_content_type == "series":
                all_content = self.series
            elif self.current_content_type == "series_episodes":
                all_content = self.series_episodes
            
            success_count = 0
            for i, item in enumerate(all_content):
                try:
                    image_path = self.download_content_image(item, self.current_content_type)
                    if image_path:
                        success_count += 1
                    
                    # تحديث الواجهة كل 10 عناصر
                    if i % 10 == 0:
                        self.root.after(0, lambda: self.download_status.config(
                            text=f"🔄 جاري تحميل الصور... ({i}/{len(all_content)})", 
                            style="Warning.TLabel"
                        ))
                        
                except Exception as e:
                    pass
            
            self.root.after(0, lambda: self.download_status.config(
                text=f"✅ تم تحميل {success_count} صورة", 
                style="Success.TLabel"
            ))
            self.root.after(0, lambda: messagebox.showinfo("نجاح", f"تم تحميل {success_count} صورة بنجاح"))
        
        threading.Thread(target=download_thread, daemon=True).start()

    def download_selected(self):
        """تحميل المحتوى المحدد"""
        if self.current_content_index == -1:
            messagebox.showwarning("تحذير", "يرجى تحديد محتوى للتحميل")
            return
        
        try:
            content_item = self.get_current_content_item()
            if not content_item:
                return
            
            content_name = content_item.get('name', 'غير معروف')
            
            # اختيار الجودة للتحميل
            quality_window = tk.Toplevel(self.root)
            quality_window.title("اختيار جودة التحميل")
            quality_window.geometry("300x200")
            quality_window.configure(bg=self.gold_colors['dark_bg'])
            quality_window.transient(self.root)
            quality_window.grab_set()
            
            ttk.Label(quality_window, text="اختر جودة التحميل:", style="Title.TLabel").pack(pady=10)
            
            download_quality_var = tk.StringVar(value="عالية (1080p)")
            quality_combo = ttk.Combobox(quality_window, textvariable=download_quality_var,
                                       values=list(self.recording_qualities.keys()),
                                       state="readonly", style="Golden.TCombobox")
            quality_combo.pack(pady=10)
            
            def start_download_with_quality():
                selected_quality = download_quality_var.get()
                quality_window.destroy()
                self.start_download_process(content_item, content_name, selected_quality)
            
            ttk.Button(quality_window, text="بدء التحميل", style="Golden.TButton",
                      command=start_download_with_quality).pack(pady=10)
            ttk.Button(quality_window, text="إلغاء", style="Golden.TButton",
                      command=quality_window.destroy).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر بدء التحميل: {str(e)}")

    def start_download_process(self, content_item, content_name, quality):
        """بدء عملية التحميل بالجودة المحددة"""
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            
            if self.current_content_type == "live":
                stream_id = content_item.get('stream_id')
                stream_url = self.get_media_url_with_advanced_detection(base_url, username, password, stream_id, "live")
                folder = self.download_folders['live']
                filename = f"{content_name}_{quality}.ts"
                
            elif self.current_content_type == "movies":
                stream_id = content_item.get('stream_id')
                stream_url = self.get_media_url_with_advanced_detection(base_url, username, password, stream_id, "movies")
                folder = self.download_folders['movies']
                filename = f"{content_name}_{quality}.mp4"
                
            elif self.current_content_type == "series_episodes":
                stream_id = content_item.get('id')
                series_name = self.content_history[-1].get('series_name', 'مسلسل')
                episode_num = content_item.get('episode_num', '0')
                season_num = content_item.get('season', '0')
                stream_url = self.get_media_url_with_advanced_detection(base_url, username, password, stream_id, "series_episodes")
                folder = os.path.join(self.download_folders['series'], series_name)
                filename = f"S{season_num}E{episode_num}_{quality}.mp4"
                
                if not os.path.exists(folder):
                    os.makedirs(folder)
            else:
                messagebox.showwarning("تحذير", "نوع المحتوى غير مدعوم للتحميل")
                return
            
            filepath = os.path.join(folder, self.sanitize_filename(filename))
            
            # إضافة للطابور
            download_item = {
                'url': stream_url,
                'filepath': filepath,
                'name': f"{content_name} ({quality})",
                'type': self.current_content_type,
                'content_item': content_item,
                'quality': quality
            }
            
            self.download_queue.append(download_item)
            self.start_download_queue()
            
            messagebox.showinfo("نجاح", f"تم إضافة {content_name} ({quality}) إلى طابور التحميل")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر بدء التحميل: {str(e)}")

    def sanitize_filename(self, filename):
        """تنظيف اسم الملف من الأحغير غير المسموحة"""
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def start_download_queue(self):
        """بدء تحميل طابور التحميل"""
        if self.downloading or not self.download_queue:
            return
        
        self.downloading = True
        self.download_thread = threading.Thread(target=self.download_worker, daemon=True)
        self.download_thread.start()

    def download_worker(self):
        """عملية التحميل الرئيسية"""
        while self.download_queue and self.downloading:
            item = self.download_queue[0]
            
            try:
                self.root.after(0, lambda: self.download_status.config(
                    text=f"⬇️ جاري تحميل: {item['name']}", 
                    style="Warning.TLabel"
                ))
                
                # تحميل الملف
                response = self.session.get(item['url'], stream=True, timeout=30, verify=False)
                total_size = int(response.headers.get('content-length', 0))
                
                downloaded = 0
                with open(item['filepath'], 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if not self.downloading:
                            break
                            
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0:
                                progress = (downloaded / total_size) * 100
                                self.root.after(0, lambda p=progress: self.update_download_progress(p))
                
                if self.downloading:
                    # حفظ معلومات المحتوى المحمل
                    self.save_downloaded_content_info(item)
                    self.download_queue.pop(0)
                    
                    self.root.after(0, lambda: self.download_status.config(
                        text=f"✅ تم تحميل: {item['name']}", 
                        style="Success.TLabel"
                    ))
                    
                    self.root.after(0, lambda: messagebox.showinfo("نجاح", f"تم تحميل {item['name']} بنجاح"))
                
            except Exception as e:
                self.root.after(0, lambda: self.download_status.config(
                    text=f"❌ فشل تحميل: {item['name']}", 
                    style="Error.TLabel"
                ))
                self.download_queue.pop(0)
        
        self.downloading = False
        self.root.after(0, lambda: self.download_status.config(
            text="💾 جاهز للتحميل", 
            style="Success.TLabel"
        ))

    def update_download_progress(self, progress):
        """تحديث شريط تقدم التحميل"""
        self.download_status.config(text=f"⬇️ جاري التحميل... {progress:.1f}%", style="Warning.TLabel")

    def save_downloaded_content_info(self, download_item):
        """حفظ معلومات المحتوى المحمل"""
        try:
            content_info = {
                'name': download_item['name'],
                'filepath': download_item['filepath'],
                'type': download_item['type'],
                'download_time': time.time(),
                'content_data': download_item['content_item'],
                'quality': download_item.get('quality', 'غير محدد')
            }
            
            content_key = hashlib.md5(download_item['name'].encode()).hexdigest()
            self.downloaded_content[download_item['type']][content_key] = content_info
            
            # حفظ في ملف
            with open('downloaded_content.json', 'w', encoding='utf-8') as f:
                json.dump(self.downloaded_content, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            pass

    def load_downloaded_content(self):
        """تحميل المحتوى المحمل"""
        try:
            if os.path.exists('downloaded_content.json'):
                with open('downloaded_content.json', 'r', encoding='utf-8') as f:
                    self.downloaded_content = json.load(f)
        except Exception as e:
            pass

    def show_downloaded_content(self):
        """عرض المحتوى المحمل"""
        downloaded_window = tk.Toplevel(self.root)
        downloaded_window.title("المحتوى المحمل")
        downloaded_window.geometry("800x600")
        downloaded_window.configure(bg=self.gold_colors['dark_bg'])
        
        # إنشاء Notebook لعرض أنواع المحتوى
        notebook = ttk.Notebook(downloaded_window, style="Custom.TFrame")
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # تبويب البث المباشر
        live_frame = ttk.Frame(notebook, style="Custom.TFrame")
        notebook.add(live_frame, text="📡 البث المباشر")
        self.create_downloaded_content_list(live_frame, 'live')
        
        # تبويب الأفلام
        movies_frame = ttk.Frame(notebook, style="Custom.TFrame")
        notebook.add(movies_frame, text="🎬 الأفلام")
        self.create_downloaded_content_list(movies_frame, 'movies')
        
        # تبويب المسلسلات
        series_frame = ttk.Frame(notebook, style="Custom.TFrame")
        notebook.add(series_frame, text="📺 المسلسلات")
        self.create_downloaded_content_list(series_frame, 'series')

    def create_downloaded_content_list(self, parent, content_type):
        """إنشاء قائمة المحتوى المحمل"""
        # شريط البحث
        search_frame = ttk.Frame(parent, style="Custom.TFrame")
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="🔍 بحث:", style="Custom.TLabel").pack(side=tk.LEFT, padx=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var, style="Golden.TEntry")
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # قائمة المحتوى
        listbox_frame = ttk.Frame(parent, style="Custom.TFrame")
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        content_listbox = tk.Listbox(listbox_frame, font=('Arial', 11),
                                   bg=self.gold_colors['medium_bg'], fg=self.gold_colors['text_primary'],
                                   selectbackground=self.gold_colors['primary'],
                                   selectforeground=self.gold_colors['dark_bg'], activestyle='none')
        
        # إضافة خاصية لتخزين المراجع
        content_listbox.content_refs = {}
        
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=content_listbox.yview)
        content_listbox.configure(yscrollcommand=scrollbar.set)
        
        content_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # أزرار التحكم
        btn_frame = ttk.Frame(parent, style="Custom.TFrame")
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="▶️ تشغيل", style="Golden.TButton",
                  command=lambda: self.play_downloaded_content(content_listbox, content_type)).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🗑️ حذف", style="Golden.TButton",
                  command=lambda: self.delete_downloaded_content(content_listbox, content_type)).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🔄 تحديث", style="Golden.TButton",
                  command=lambda: self.refresh_downloaded_list(content_listbox, content_type)).pack(side=tk.LEFT, padx=2)
        
        # تعبئة القائمة
        self.refresh_downloaded_list(content_listbox, content_type)
        
        # ربط البحث
        def search_downloaded(*args):
            self.search_downloaded_content(content_listbox, content_type, search_var.get())
        
        search_var.trace('w', search_downloaded)

    def refresh_downloaded_list(self, listbox, content_type):
        """تحديث قائمة المحتوى المحمل"""
        listbox.delete(0, tk.END)
        listbox.content_refs.clear()
        
        content_items = self.downloaded_content.get(content_type, {})
        for key, item in content_items.items():
            name = item.get('name', 'غير معروف')
            filepath = item.get('filepath', '')
            quality = item.get('quality', '')
            
            if os.path.exists(filepath):
                display_name = f"{name} | {quality}" if quality else name
                listbox.insert(tk.END, display_name)
                # تخزين المرجع
                listbox.content_refs[listbox.size()-1] = key
            else:
                # حذف العناصر التالفة
                del self.downloaded_content[content_type][key]
        
        # حفظ التغييرات
        self.save_downloaded_content_info({})

    def search_downloaded_content(self, listbox, content_type, search_term):
        """بحث في المحتوى المحمل"""
        listbox.delete(0, tk.END)
        listbox.content_refs.clear()
        
        content_items = self.downloaded_content.get(content_type, {})
        for key, item in content_items.items():
            name = item.get('name', 'غير معروف')
            filepath = item.get('filepath', '')
            quality = item.get('quality', '')
            
            if search_term.lower() in name.lower() and os.path.exists(filepath):
                index = listbox.size()
                display_name = f"{name} | {quality}" if quality else name
                listbox.insert(tk.END, display_name)
                listbox.content_refs[index] = key

    def play_downloaded_content(self, listbox, content_type):
        """تشغيل المحتوى المحمل"""
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد محتوى للتشغيل")
            return
        
        index = selection[0]
        content_key = listbox.content_refs.get(index)
        if not content_key:
            return
        
        content_item = self.downloaded_content[content_type][content_key]
        filepath = content_item.get('filepath')
        
        if not os.path.exists(filepath):
            messagebox.showerror("خطأ", "الملف غير موجود")
            return
        
        try:
            # تشغيل الملف المحلي
            self.play_local_file(filepath, content_item.get('name', 'محتوى محمل'))
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تشغيل الملف: {str(e)}")

    def play_local_file(self, filepath, title):
        """تشغيل ملف محلي"""
        try:
            if self.media_player.is_playing():
                self.media_player.stop()
            
            media = self.instance.media_new(filepath)
            
            # إعدادات للملفات المحلية
            media_options = [
                '--file-caching=3000',
                '--codec=avcodec',
                '--avcodec-hw=any',
                '--avcodec-threads=4',
                '--audio-resampler=soxr',
                '--audio-channels=2',
                '--deinterlace=1',
                '--no-video-title-show',
                '--no-stats',
                '--no-osd'
            ]
            
            for option in media_options:
                media.add_option(option)
            
            self.media_player.set_media(media)
            self.set_vlc_window()
            
            result = self.media_player.play()
            
            if result == -1:
                messagebox.showerror("خطأ", "تعذر تشغيل الملف المحلي")
                return
            
            self.info_label.config(text=f"📺 {title} (محلي)")
            self.play_status.config(text="▶️ قيد التشغيل", style="Success.TLabel")
            self.set_volume(self.volume_var.get())
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تشغيل الملف: {str(e)}")

    def delete_downloaded_content(self, listbox, content_type):
        """حذف المحتوى المحمل"""
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى تحديد محتوى للحذف")
            return
        
        index = selection[0]
        content_key = listbox.content_refs.get(index)
        if not content_key:
            return
        
        content_item = self.downloaded_content[content_type][content_key]
        filepath = content_item.get('filepath')
        
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            
            del self.downloaded_content[content_type][content_key]
            
            # حفظ التغييرات
            self.save_downloaded_content_info({})
            
            # تحديث القائمة
            self.refresh_downloaded_list(listbox, content_type)
            
            messagebox.showinfo("نجاح", "تم حذف المحتوى بنجاح")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر حذف الملف: {str(e)}")

    def get_current_content_item(self):
        """الحصول على عنصر المحتوى الحالي"""
        if self.current_content_type == "live" and 0 <= self.current_content_index < len(self.channels):
            return self.channels[self.current_content_index]
        elif self.current_content_type == "movies" and 0 <= self.current_content_index < len(self.movies):
            return self.movies[self.current_content_index]
        elif self.current_content_type == "series_episodes" and 0 <= self.current_content_index < len(self.series_episodes):
            return self.series_episodes[self.current_content_index]
        elif self.current_content_type == "series" and 0 <= self.current_content_index < len(self.series):
            return self.series[self.current_content_index]
        return None

    def show_content_image(self):
        """عرض صورة المحتوى المحدد"""
        content_item = self.get_current_content_item()
        if not content_item:
            return
        
        try:
            image_path = self.download_content_image(content_item, self.current_content_type)
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize((200, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                self.info_image_label.configure(image=photo)
                self.info_image_label.image = photo
            else:
                self.info_image_label.configure(image='')
                self.info_image_label.image = None
                
        except Exception as e:
            self.info_image_label.configure(image='')
            self.info_image_label.image = None

    # الدوال الأساسية للمشغل
    def get_media_url_with_advanced_detection(self, base_url, username, password, stream_id, content_type):
        """الحصول على رابط التشغيل مع الاكتشاف المتقدم للتنسيقات"""
        try:
            if content_type == "live":
                url_template = f"{base_url}/live/{username}/{password}/{stream_id}"
            elif content_type == "movies":
                url_template = f"{base_url}/movie/{username}/{password}/{stream_id}"
            elif content_type == "series_episodes":
                url_template = f"{base_url}/series/{username}/{password}/{stream_id}"
            else:
                return None
            
            best_url = self.advanced_format_detection(url_template)
            return best_url if best_url else url_template
            
        except Exception as e:
            return None

    def advanced_format_detection(self, base_url):
        """اكتشاف متقدم لجميع تنسيقات الوسائط الحديثة"""
        modern_formats = [
            '', '.ts', '.m2ts', '.mts', '.mpg', '.mpeg', '.ts?', '.ts&',
            '.m3u8', '.m3u', '.m3u?', '.m3u&',
            '.mp4', '.mp4?', '.mp4&', '.m4v', '.m4v?', '.m4v&',
            '.mkv', '.mkv?', '.mkv&', '.mk3d',
            '.avi', '.avi?', '.avi&', '.divx',
            '.mov', '.mov?', '.mov&', '.qt',
            '.wmv', '.wmv?', '.wmv&', '.asf',
            '.flv', '.flv?', '.flv&', '.f4v',
            '.webm', '.webm?', '.webm&',
            '.rm', '.rmvb', '.ram',
            '.ogv', '.ogg',
            '.3gp', '.3g2', '.vob', '.dat', '.strm',
            '?token=', '&token=', '?secret=', '&secret=',
            '?auth=', '&auth=', '?key=', '&key='
        ]
        
        for fmt in modern_formats:
            test_url = f"{base_url}{fmt}" if fmt else base_url
            
            if '?' in base_url and fmt.startswith('?'):
                continue
            if '&' in base_url and fmt.startswith('&'):
                continue
                
            try:
                response = self.session.head(test_url, timeout=2, verify=False, allow_redirects=True)
                
                content_type = response.headers.get('content-type', '').lower()
                is_video_content = any(video_type in content_type for video_type in [
                    'video/', 'application/x-mpegurl', 'application/vnd.apple.mpegurl',
                    'audio/', 'application/octet-stream'
                ])
                
                if response.status_code in [200, 206] or is_video_content:
                    return test_url
                    
            except:
                continue
        
        return base_url

    def play_video_advanced(self, url, title):
        """تشغيل الفيديو بإعدادات متقدمة حديثة مع دعم الجودة"""
        try:
            if self.media_player.is_playing():
                self.media_player.stop()
            
            media = self.instance.media_new(url)
            
            media_options = [
                '--network-caching=5000',
                '--file-caching=5000', 
                '--live-caching=4000',
                '--sout-mux-caching=2000',
                '--codec=avcodec',
                '--avcodec-hw=any',
                '--avcodec-threads=4',
                '--avcodec-skiploopfilter=0',
                '--avcodec-skip-frame=0',
                '--avcodec-skip-idct=0',
                '--adaptive-logic=rate',
                '--clock-jitter=0',
                '--clock-synchro=0',
                '--drop-late-frames',
                '--skip-frames',
                '--demux=avformat',
                '--avformat-format=mp4,ts,avi,mkv,flv,webm,mov,m3u8',
                '--avformat-options=rtsp_transport=tcp',
                '--audio-resampler=soxr',
                '--audio-channels=2',
                '--audio-replay-gain-mode=track',
                '--deinterlace=1',
                '--deinterlace-mode=blend',
                '--video-filter=deinterlace',
                '--h264-fps=60',
                f'--http-user-agent={self.session.headers["User-Agent"]}',
                '--http-reconnect',
                '--http-continuous',
                '--http-persistent',
                '--rtsp-tcp',
                '--rtp-client-port=5000',
                '--no-video-title-show',
                '--no-stats',
                '--no-osd',
                '--no-snapshot-preview',
                '--no-interact',
                '--no-loop',
                '--no-video-on-top',
                '--disable-screensaver',
                '--quiet'
            ]
            
            # إضافة إعدادات الجودة إذا كانت محددة
            if self.current_quality != "auto":
                media_options.extend([
                    f'--sout-x264-preset=medium',
                    f'--sout-x264-tune=film',
                    f'--sout-x264-crf=23'
                ])
            
            for option in media_options:
                media.add_option(option)
            
            self.media_player.set_media(media)
            self.set_vlc_window()
            
            result = self.media_player.play()
            
            if result == -1:
                self.play_video_simple(url, title)
                return
            
            if self.show_channel_info:
                quality_text = f" | الجودة: {self.quality_var.get()}" if self.current_quality != "auto" else ""
                self.info_label.config(text=f"📺 {title}{quality_text}")
                self.stream_info.config(text=f"🔗 {url[:80]}...")
            else:
                self.info_label.config(text="🔒 المعلومات مخفية")
                self.stream_info.config(text="")
            
            self.play_status.config(text="▶️ قيد التشغيل", style="Success.TLabel")
            self.set_volume(self.volume_var.get())
            
            self.content_history.append({
                'content_type': 'playback',
                'title': title,
                'url': url,
                'quality': self.current_quality
            })
            self.update_path_label()
            
            self.root.after(1000, self.check_playback_status)
            
        except Exception as e:
            self.play_video_simple(url, title)

    def play_video_simple(self, url, title):
        """طريقة تشغيل مبسطة كبديل احتياطي"""
        try:
            if self.media_player.is_playing():
                self.media_player.stop()
            
            media = self.instance.media_new(url)
            
            simple_options = [
                '--network-caching=3000',
                '--file-caching=3000',
                '--live-caching=2000',
                '--http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                '--http-reconnect',
                '--rtsp-tcp',
                '--no-video-title-show'
            ]
            
            for option in simple_options:
                media.add_option(option)
            
            self.media_player.set_media(media)
            self.set_vlc_window()
            
            result = self.media_player.play()
            
            if result == -1:
                messagebox.showerror("خطأ", "تعذر تشغيل الملف. قد يكون التنسيق غير مدعوم أو الرابط غير صالح.")
                return
            
            self.info_label.config(text=f"📺 {title} (الوضع المتوافق)")
            self.play_status.config(text="▶️ قيد التشغيل (متوافق)", style="Warning.TLabel")
            self.set_volume(self.volume_var.get())
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تشغيل الفيديو: {str(e)}")

    def play_current_content(self):
        """تشغيل المحتوى المحدد مع الاكتشاف التلقائي للتنسيق"""
        if self.current_content_index == -1:
            return
            
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            
            if self.current_content_type == "live":
                channel = self.channels[self.current_content_index]
                stream_id = channel.get('stream_id')
                content_name = channel.get('name', 'غير معروف')
                stream_url = self.get_media_url_with_advanced_detection(base_url, username, password, stream_id, "live")
                
            elif self.current_content_type == "movies":
                movie = self.movies[self.current_content_index]
                stream_id = movie.get('stream_id')
                content_name = movie.get('name', 'غير معروف')
                stream_url = self.get_media_url_with_advanced_detection(base_url, username, password, stream_id, "movies")
                
            elif self.current_content_type == "series_episodes":
                episode = self.series_episodes[self.current_content_index]
                stream_id = episode.get('id')
                content_name = f"{episode.get('title', 'غير معروف')} - S{episode.get('season', '0')}E{episode.get('episode_num', '0')}"
                stream_url = self.get_media_url_with_advanced_detection(base_url, username, password, stream_id, "series_episodes")
                
            else:
                return
            
            if not stream_url:
                messagebox.showerror("خطأ", "تعذر الحصول على رابط التشغيل")
                return
            
            self.current_media_url = stream_url
            self.play_video_advanced(stream_url, content_name)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تشغيل المحتوى: {str(e)}")

    def set_vlc_window(self):
        """تعيين نافذة VLC"""
        try:
            if sys.platform.startswith('win'):
                self.media_player.set_hwnd(self.video_panel.winfo_id())
            elif sys.platform.startswith('linux'):
                self.media_player.set_xwindow(self.video_panel.winfo_id())
            elif sys.platform.startswith('darwin'):
                self.media_player.set_nsobject(self.video_panel.winfo_id())
        except Exception as e:
            pass

    def pause_video(self):
        """إيقاف الفيديو مؤقتاً"""
        if self.media_player.is_playing():
            self.media_player.pause()
            self.play_status.config(text="⏸️ متوقف مؤقتاً")

    def play_video_current(self):
        """استئناف تشغيل الفيديو الحالي"""
        if not self.media_player.is_playing():
            self.media_player.play()
            self.play_status.config(text="▶️ قيد التشغيل")

    def stop_video(self):
        """إيقاف الفيديو"""
        self.media_player.stop()
        self.play_status.config(text="⏹️ متوقف")
        self.progress_var.set(0)
        self.progress_label.config(text="00:00 / 00:00")

    def toggle_mute(self):
        """كتم/إلغاء كتم الصوت"""
        is_muted = self.media_player.audio_get_mute()
        self.media_player.audio_set_mute(not is_muted)

    def volume_up(self):
        """زيادة الصوت"""
        volume = self.media_player.audio_get_volume()
        self.media_player.audio_set_volume(min(volume + 10, 100))
        self.volume_var.set(self.media_player.audio_get_volume())

    def volume_down(self):
        """خفض الصوت"""
        volume = self.media_player.audio_get_volume()
        self.media_player.audio_set_volume(max(volume - 10, 0))
        self.volume_var.set(self.media_player.audio_get_volume())

    def set_volume(self, value):
        """ضبط مستوى الصوت"""
        volume = int(value)
        self.media_player.audio_set_volume(volume)

    def seek_relative(self, seconds):
        """التقدم أو التراجع بثوانٍ"""
        if self.media_player.is_playing():
            current_time = self.media_player.get_time() + (seconds * 1000)
            self.media_player.set_time(int(current_time))

    def seek_video(self, value):
        """التقدم إلى وقت محدد"""
        if self.media_player.is_playing():
            media_length = self.media_player.get_length()
            if media_length > 0:
                seek_time = (float(value) / 100) * media_length
                self.media_player.set_time(int(seek_time))

    def previous_content(self):
        """الانتقال إلى المحتوى السابق"""
        if self.current_content_type in ["live", "movies", "series_episodes"]:
            if self.current_content_index > 0:
                self.current_content_index -= 1
                self.content_listbox.selection_clear(0, tk.END)
                self.content_listbox.selection_set(self.current_content_index)
                self.content_listbox.see(self.current_content_index)
                self.play_current_content()

    def next_content(self):
        """الانتقال إلى المحتوى التالي"""
        if self.current_content_type == "live":
            max_index = len(self.channels) - 1
        elif self.current_content_type == "movies":
            max_index = len(self.movies) - 1
        elif self.current_content_type == "series_episodes":
            max_index = len(self.series_episodes) - 1
        else:
            return
            
        if self.current_content_index < max_index:
            self.current_content_index += 1
            self.content_listbox.selection_clear(0, tk.END)
            self.content_listbox.selection_set(self.current_content_index)
            self.content_listbox.see(self.current_content_index)
            self.play_current_content()

    def restart_video(self):
        """إعادة تشغيل الفيديو من البداية"""
        if self.media_player.is_playing():
            self.media_player.set_time(0)

    def update_progress(self):
        """تحديث شريط التقدم"""
        try:
            if self.media_player.is_playing():
                current_time = self.media_player.get_time() / 1000
                total_duration = self.media_player.get_length() / 1000
                if total_duration > 0:
                    progress_percent = (current_time / total_duration) * 100
                    self.progress_var.set(progress_percent)
                    current_str = self.format_time(current_time)
                    total_str = self.format_time(total_duration)
                    self.progress_label.config(text=f"{current_str} / {total_str}")
        except:
            pass
        finally:
            self.root.after(1000, self.update_progress)

    def format_time(self, seconds):
        """تنسيق الوقت"""
        if seconds < 0:
            return "00:00"
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def check_playback_status(self):
        """مراقبة حالة التشغيل"""
        try:
            if self.media_player.is_playing():
                state = self.media_player.get_state()
                
                if state == vlc.State.Error:
                    self.play_status.config(text="❌ خطأ في التشغيل", style="Error.TLabel")
                elif state == vlc.State.Playing:
                    self.root.after(2000, self.check_playback_status)
                elif state == vlc.State.Buffering:
                    self.play_status.config(text="🔄 جاري التحميل...", style="Warning.TLabel")
                    self.root.after(1000, self.check_playback_status)
                    
        except Exception as e:
            pass

    def toggle_channel_info(self):
        """تبديل إظهار/إخفاء معلومات القناة"""
        self.show_channel_info = not self.show_channel_info
        if not self.show_channel_info:
            self.info_label.config(text="🔒 المعلومات مخفية", foreground="gray")
            self.stream_info.config(text="")
        else:
            if hasattr(self, 'current_content_index') and self.current_content_index >= 0:
                self.preview_content(self.current_content_index)

    def preview_content(self, index):
        """معاينة المحتوى"""
        content_list = self.get_current_content()
        if 0 <= index < len(content_list):
            item = content_list[index]
            if self.show_channel_info:
                self.info_label.config(text=f"📡 جاهز: {item['name']}", foreground="green")
                if 'url' in item:
                    self.stream_info.config(text=f"🔗 ...{item['url'][-30:]}")
                else:
                    self.stream_info.config(text="📺 مسلسل - انقر نقراً مزدوجاً لعرض الحلقات")

    def get_current_content(self):
        """الحصول على المحتوى الحالي"""
        if self.current_content_type == "live":
            return self.channels
        elif self.current_content_type == "movies":
            return self.movies
        elif self.current_content_type == "series" and self.series_episodes:
            return self.series_episodes
        elif self.current_content_type == "series":
            return self.series
        else:
            return []

    def toggle_player_fullscreen(self):
        """تبديل وضع ملء الشاشة"""
        if not self.is_player_fullscreen:
            self.enter_player_fullscreen()
        else:
            self.exit_player_fullscreen()

    def enter_player_fullscreen(self):
        """الدخول إلى وضع ملء الشاشة"""
        try:
            self.is_player_fullscreen = True
            self.is_playing_before_fullscreen = self.media_player.is_playing()
            self.current_playback_time = self.media_player.get_time()
            
            self.settings_frame.pack_forget()
            self.control_bar.pack_forget()
            self.left_frame.pack_forget()
            self.info_frame.pack_forget()
            self.progress_frame.pack_forget()
            
            self.video_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
            self.video_panel.pack(fill=tk.BOTH, expand=True)
            
            self.root.attributes('-fullscreen', True)
            self.root.after(100, self.reinitialize_vlc_after_fullscreen)
            
        except Exception as e:
            self.exit_player_fullscreen()

    def exit_player_fullscreen(self):
        """الخروج من وضع ملء الشاشة"""
        try:
            self.is_player_fullscreen = False
            self.is_playing_before_fullscreen = self.media_player.is_playing()
            self.current_playback_time = self.media_player.get_time()
            
            self.root.attributes('-fullscreen', False)
            self.restore_normal_layout()
            self.root.after(100, self.reinitialize_vlc_after_exit_fullscreen)
            
        except Exception as e:
            pass

    def reinitialize_vlc_after_fullscreen(self):
        """إعادة تهيئة VLC بعد الدخول لملء الشاشة"""
        try:
            self.set_vlc_window()
            if self.is_playing_before_fullscreen and self.current_media_url:
                self.root.after(500, self.restore_playback_after_fullscreen)
        except Exception as e:
            pass

    def reinitialize_vlc_after_exit_fullscreen(self):
        """إعادة تهيئة VLC بعد الخروج من ملء الشاشة"""
        try:
            self.set_vlc_window()
            if self.is_playing_before_fullscreen and self.current_media_url:
                self.root.after(500, self.restore_playback_after_exit_fullscreen)
        except Exception as e:
            pass

    def restore_playback_after_fullscreen(self):
        """استعادة التشغيل بعد الدخول لملء الشاشة"""
        try:
            if self.current_media_url:
                media = self.instance.media_new(self.current_media_url)
                media.add_option(f'--http-user-agent={self.session.headers["User-Agent"]}')
                self.media_player.set_media(media)
                
                if self.media_player.play() == -1:
                    pass
                else:
                    if self.current_playback_time > 0:
                        self.root.after(1000, lambda: self.media_player.set_time(self.current_playback_time))
        except Exception as e:
            pass

    def restore_playback_after_exit_fullscreen(self):
        """استعادة التشغيل بعد الخروج من ملء الشاشة"""
        try:
            if self.current_media_url:
                media = self.instance.media_new(self.current_media_url)
                media.add_option(f'--http-user-agent={self.session.headers["User-Agent"]}')
                self.media_player.set_media(media)
                
                if self.media_player.play() == -1:
                    pass
                else:
                    if self.current_playback_time > 0:
                        self.root.after(1000, lambda: self.media_player.set_time(self.current_playback_time))
        except Exception as e:
            pass

    def restore_normal_layout(self):
        """استعادة التخطيط العادي"""
        try:
            self.settings_frame.pack(fill=tk.X, padx=10, pady=5)
            self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
            self.video_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            self.video_panel.pack(fill=tk.BOTH, expand=True)
            self.info_frame.pack(fill=tk.X, pady=5)
            self.progress_frame.pack(fill=tk.X, pady=5)
            
            self.control_bar.pack(fill=tk.X, padx=10, pady=5)
            
        except Exception as e:
            pass

    def hide_all_category_frames(self):
        """إخفاء جميع إطارات التصنيفات"""
        self.cat_frame.pack_forget()
        self.series_cat_frame.pack_forget()
        self.movies_cat_frame.pack_forget()

    def show_category_frames(self, content_type):
        """إظهار إطارات التصنيفات المناسبة"""
        self.hide_all_category_frames()
        if content_type == "live":
            self.cat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        elif content_type == "series":
            self.series_cat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        elif content_type == "movies":
            self.movies_cat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

    def toggle_auto_save(self):
        self.auto_save_credentials = self.save_var.get()
        if self.auto_save_credentials:
            self.save_status.config(text="💾 الحفظ مفعل", style="Success.TLabel")
            self.save_credentials()
        else:
            self.save_status.config(text="💾 الحفظ معطل", style="Error.TLabel")

    def save_credentials(self):
        if not self.auto_save_credentials:
            return False
        try:
            username = self.user_entry.get().strip()
            password = self.pass_entry.get().strip()
            
            if not username or not password:
                return False
                
            config_data = {
                'username': self.encrypt_data(username),
                'password': self.encrypt_data(password),
                'auto_save': self.auto_save_credentials,
                'timestamp': time.time()
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f)
            
            return True
        except Exception as e:
            return False

    def load_saved_credentials(self):
        try:
            if not os.path.exists(self.config_file):
                return False
                
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            username = self.decrypt_data(config_data['username'])
            password = self.decrypt_data(config_data['password'])
            
            self.user_entry.delete(0, tk.END)
            self.user_entry.insert(0, username)
            self.pass_entry.delete(0, tk.END)
            self.pass_entry.insert(0, password)
            
            self.auto_save_credentials = config_data.get('auto_save', True)
            self.save_var.set(self.auto_save_credentials)
            
            if self.auto_save_credentials:
                self.save_status.config(text="💾 الحفظ مفعل", style="Success.TLabel")
            else:
                self.save_status.config(text="💾 الحفظ معطل", style="Error.TLabel")
            
            return True
            
        except Exception as e:
            return False

    def clear_saved_credentials(self):
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            
            self.user_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)
            
            self.auto_save_credentials = True
            self.save_var.set(True)
            self.save_status.config(text="💾 الحفظ مفعل", style="Success.TLabel")
            
            messagebox.showinfo("نجاح", "تم مسح البيانات المحفوظة بنجاح")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر مسح البيانات: {str(e)}")

    def show_saved_username(self):
        try:
            if not os.path.exists(self.config_file):
                messagebox.showinfo("اليوزر المخزن", "لا يوجد بيانات مخزنة")
                return
                
            with open(self.config_file, 'r') as f:
                config_data = json.load(f)
            
            username = self.decrypt_data(config_data['username'])
            timestamp = config_data.get('timestamp', 0)
            
            if timestamp:
                save_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
                message = f"اسم المستخدم المخزن:\n{username}\n\nتم الحفظ في: {save_time}"
            else:
                message = f"اسم المستخدم المخزن:\n{username}"
                
            messagebox.showinfo("اليوزر المخزن", message)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر تحميل البيانات: {str(e)}")

    def get_cache_key(self, url, params=None):
        key_string = url
        if params:
            key_string += str(params)
        return hashlib.md5(key_string.encode()).hexdigest()

    def save_to_cache(self, key, data, cache_type="data"):
        if not self.cache_enabled:
            return False
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}_{cache_type}.cache")
            cache_data = {
                'timestamp': time.time(),
                'data': data,
                'type': cache_type
            }
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
            return True
        except Exception as e:
            return False

    def load_from_cache(self, key, cache_type="data", max_age=None):
        if not self.cache_enabled:
            return None
        if max_age is None:
            max_age = self.cache_duration
        try:
            cache_file = os.path.join(self.cache_dir, f"{key}_{cache_type}.cache")
            if not os.path.exists(cache_file):
                return None
            
            with open(cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            if time.time() - cache_data['timestamp'] > max_age:
                os.remove(cache_file)
                return None
            
            return cache_data['data']
        except Exception as e:
            return None

    def clear_cache(self):
        try:
            for filename in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            messagebox.showinfo("نجاح", "تم مسح بيانات الكاش بنجاح")
            self.cache_status.config(text="💾 الكاش مفعل (مُفرغ)", style="Warning.TLabel")
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر مسح الكاش: {str(e)}")

    def toggle_cache(self):
        self.cache_enabled = not self.cache_enabled
        if self.cache_enabled:
            self.cache_status.config(text="💾 الكاش مفعل", style="Success.TLabel")
            messagebox.showinfo("الكاش", "تم تفعيل نظام الكاش")
        else:
            self.cache_status.config(text="💾 الكاش معطل", style="Error.TLabel")
            messagebox.showinfo("الكاش", "تم تعطيل نظام الكاش")

    def monitor_server_status(self):
        if self.server_config['username'] and self.server_config['password']:
            try:
                username = self.decrypt_data(self.server_config['username'])
                password = self.decrypt_data(self.server_config['password'])
                base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
                
                status_key = self.get_cache_key(f"server_status_{username}")
                cached_status = self.load_from_cache(status_key, "status", max_age=60)
                
                if cached_status is None:
                    auth_url = f"{base_url}/player_api.php?username={username}&password={password}"
                    response = self.session.get(auth_url, timeout=5, verify=False)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('user_info', {}).get('auth') == 1:
                            self.server_status = "online"
                            self.server_status_label.config(text="🟢 السيرفر متصل", style="Success.TLabel")
                            self.save_to_cache(status_key, "online", "status")
                        else:
                            self.server_status = "auth_failed"
                            self.server_status_label.config(text="🟡 خطأ في المصادقة", style="Warning.TLabel")
                    else:
                        self.server_status = "offline"
                        self.server_status_label.config(text="🔴 السيرفر غير متاح", style="Error.TLabel")
                else:
                    self.server_status = cached_status
                    if cached_status == "online":
                        self.server_status_label.config(text="🟢 السيرفر متصل", style="Success.TLabel")
                    else:
                        self.server_status_label.config(text="🔴 السيرفر غير متاح", style="Error.TLabel")
                        
            except Exception as e:
                self.server_status = "offline"
                self.server_status_label.config(text="🔴 السيرفر غير متاح", style="Error.TLabel")
        
        self.root.after(30000, self.monitor_server_status)

    def check_server_status(self):
        self.monitor_server_status()
        status_messages = {
            "online": "🟢 السيرفر متصل ويعمل بشكل طبيعي",
            "offline": "🔴 السيرفر غير متاح حالياً",
            "auth_failed": "🟡 خطأ في المصادقة - تحقق من البيانات"
        }
        message = status_messages.get(self.server_status, "🟠 حالة غير معروفة")
        messagebox.showinfo("حالة السيرفر", message)

    def reconnect_server(self):
        self.connection_status.config(text="🔄 جاري إعادة الاتصال...", style="Warning.TLabel")
        self.root.update()
        
        if self.connect_server():
            messagebox.showinfo("نجاح", "تم إعادة الاتصال بالسيرفر بنجاح")
        else:
            messagebox.showerror("خطأ", "فشل إعادة الاتصال بالسيرفر")

    def get_cached_data_with_fallback(self, url, cache_key, cache_type="data", timeout=10):
        cached_data = self.load_from_cache(cache_key, cache_type)
        if cached_data is not None:
            return cached_data
        
        try:
            response = self.session.get(url, timeout=timeout, verify=False)
            if response.status_code == 200:
                data = response.json()
                self.save_to_cache(cache_key, data, cache_type)
                return data
            else:
                raise Exception(f"خطأ في الاستجابة: {response.status_code}")
                
        except Exception as e:
            old_cached_data = self.load_from_cache(cache_key, cache_type, max_age=86400)
            if old_cached_data is not None:
                return old_cached_data
            return None

    def toggle_username_visibility(self):
        self.show_username = not self.show_username
        if self.show_username:
            self.user_entry.config(show="")
            self.show_user_btn.config(text="🙈")
        else:
            self.user_entry.config(show="*")
            self.show_user_btn.config(text="👁️")

    def encrypt_data(self, data):
        try:
            fernet = Fernet(base64.urlsafe_b64encode(self.encryption_key.ljust(32)[:32]))
            encrypted_data = fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            return data

    def decrypt_data(self, encrypted_data):
        try:
            fernet = Fernet(base64.urlsafe_b64encode(self.encryption_key.ljust(32)[:32]))
            decrypted_data = fernet.decrypt(base64.urlsafe_b64decode(encrypted_data))
            return decrypted_data.decode()
        except Exception as e:
            return encrypted_data

    def get_server_config(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        self.server_config = {
            'host': 'tv.nv2.info',
            'port': '80',
            'username': self.encrypt_data(username),
            'password': self.encrypt_data(password),
            'type': 'xtream'
        }
        
        if username and password and self.auto_save_credentials:
            self.save_credentials()

    def validate_config(self):
        self.get_server_config()
        
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
        except:
            username = self.server_config['username']
            password = self.server_config['password']
            
        if not all([username, password]):
            messagebox.showwarning("تحذير", "يرجى إدخال اسم المستخدم وكلمة المرور")
            return False
        return True

    def connect_server(self):
        if not self.validate_config():
            return
            
        self.connection_status.config(text="🔄 جاري الاتصال...", style="Warning.TLabel")
        self.root.update()
        
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            auth_url = f"{base_url}/player_api.php?username={username}&password={password}"
            
            response = self.session.get(auth_url, timeout=10, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get('user_info', {}).get('auth') == 1:
                    self.connection_status.config(text="✅ متصل", style="Success.TLabel")
                    messagebox.showinfo("نجاح", "تم الاتصال بالسيرفر بنجاح!")
                    self.load_live_categories(base_url, username, password)
                    self.load_series_categories(base_url, username, password)
                    self.load_movies_categories(base_url, username, password)
                    self.content_history = [{
                        'content_type': 'live', 'series_episodes': [],
                        'current_series_id': None, 'title': 'البث المباشر'
                    }]
                    self.update_path_label()
                    
                    if self.auto_save_credentials:
                        self.save_credentials()
                        
                    return True
                    
            self.connection_status.config(text="❌ فشل الاتصال", style="Error.TLabel")
            return False
            
        except Exception as e:
            self.connection_status.config(text="❌ خطأ اتصال", style="Error.TLabel")
            messagebox.showerror("خطأ", f"تعذر الاتصال: {str(e)}")
            return False

    def load_live_categories(self, base_url, username, password):
        try:
            cache_key = self.get_cache_key(f"live_categories_{username}")
            categories_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_live_categories"
            
            data = self.get_cached_data_with_fallback(categories_url, cache_key, "categories")
            if data:
                self.categories = data
                self.cat_listbox.delete(0, tk.END)
                for cat in self.categories:
                    self.cat_listbox.insert(tk.END, cat.get('category_name', 'غير معروف'))
            else:
                messagebox.showerror("خطأ", "تعذر تحميل تصنيفات البث المباشر")
        except Exception as e:
            pass

    def load_series_categories(self, base_url, username, password):
        try:
            cache_key = self.get_cache_key(f"series_categories_{username}")
            categories_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_series_categories"
            
            data = self.get_cached_data_with_fallback(categories_url, cache_key, "series_categories")
            if data:
                self.series_categories = data
                self.series_cat_listbox.delete(0, tk.END)
                for cat in self.series_categories:
                    self.series_cat_listbox.insert(tk.END, cat.get('category_name', 'غير معروف'))
        except Exception as e:
            pass

    def load_movies_categories(self, base_url, username, password):
        try:
            cache_key = self.get_cache_key(f"movies_categories_{username}")
            categories_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_vod_categories"
            
            data = self.get_cached_data_with_fallback(categories_url, cache_key, "movies_categories")
            if data:
                self.movies_categories = data
                self.movies_cat_listbox.delete(0, tk.END)
                for cat in self.movies_categories:
                    self.movies_cat_listbox.insert(tk.END, cat.get('category_name', 'غير معروف'))
        except Exception as e:
            pass

    def on_category_select(self, event):
        if not self.cat_listbox.curselection():
            return
            
        index = self.cat_listbox.curselection()[0]
        category_id = self.categories[index].get('category_id')
        category_name = self.categories[index].get('category_name')
        
        self.load_live_streams(category_id, category_name)

    def on_series_category_select(self, event):
        if not self.series_cat_listbox.curselection():
            return
            
        index = self.series_cat_listbox.curselection()[0]
        category_id = self.series_categories[index].get('category_id')
        category_name = self.series_categories[index].get('category_name')
        
        self.load_series(category_id, category_name)

    def on_movies_category_select(self, event):
        if not self.movies_cat_listbox.curselection():
            return
            
        index = self.movies_cat_listbox.curselection()[0]
        category_id = self.movies_categories[index].get('category_id')
        category_name = self.movies_categories[index].get('category_name')
        
        self.load_movies_by_category(category_id, category_name)

    def load_live_streams(self, category_id, category_name):
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            
            cache_key = self.get_cache_key(f"live_streams_{category_id}_{username}")
            streams_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_live_streams&category_id={category_id}"
            
            data = self.get_cached_data_with_fallback(streams_url, cache_key, "streams")
            if data:
                self.channels = data
                self.current_content_type = "live"
                self.content_listbox.delete(0, tk.END)
                for channel in self.channels:
                    self.content_listbox.insert(tk.END, channel.get('name', 'غير معروف'))
                
                self.content_frame.config(text=f"📺 {category_name} ({len(self.channels)})")
                self.show_category_frames("live")
                
                self.content_history.append({
                    'content_type': 'live',
                    'category_id': category_id,
                    'category_name': category_name,
                    'series_episodes': [],
                    'current_series_id': None,
                    'title': category_name
                })
                self.update_path_label()
                
        except Exception as e:
            pass

    def load_series(self, category_id, category_name):
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            
            cache_key = self.get_cache_key(f"series_{category_id}_{username}")
            series_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_series&category_id={category_id}"
            
            data = self.get_cached_data_with_fallback(series_url, cache_key, "series")
            if data:
                self.series = data
                self.current_content_type = "series"
                self.content_listbox.delete(0, tk.END)
                for series in self.series:
                    self.content_listbox.insert(tk.END, series.get('name', 'غير معروف'))
                
                self.content_frame.config(text=f"📺 مسلسلات {category_name} ({len(self.series)})")
                self.show_category_frames("series")
                
                self.content_history.append({
                    'content_type': 'series',
                    'category_id': category_id,
                    'category_name': category_name,
                    'series_episodes': [],
                    'current_series_id': None,
                    'title': f"مسلسلات {category_name}"
                })
                self.update_path_label()
                
        except Exception as e:
            pass

    def load_movies_by_category(self, category_id, category_name):
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            
            cache_key = self.get_cache_key(f"movies_{category_id}_{username}")
            movies_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_vod_streams&category_id={category_id}"
            
            data = self.get_cached_data_with_fallback(movies_url, cache_key, "movies")
            if data:
                self.movies = data
                self.current_content_type = "movies"
                self.content_listbox.delete(0, tk.END)
                for movie in self.movies:
                    self.content_listbox.insert(tk.END, movie.get('name', 'غير معروف'))
                
                self.content_frame.config(text=f"🎬 أفلام {category_name} ({len(self.movies)})")
                self.show_category_frames("movies")
                
                self.content_history.append({
                    'content_type': 'movies',
                    'category_id': category_id,
                    'category_name': category_name,
                    'series_episodes': [],
                    'current_series_id': None,
                    'title': f"أفلام {category_name}"
                })
                self.update_path_label()
                
        except Exception as e:
            pass

    def load_series_episodes(self, series_id, series_name):
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            
            cache_key = self.get_cache_key(f"series_episodes_{series_id}_{username}")
            episodes_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_series_info&series_id={series_id}"
            
            data = self.get_cached_data_with_fallback(episodes_url, cache_key, "episodes")
            if data:
                episodes = data.get('episodes', {})
                self.series_episodes = []
                
                for season_num, season_episodes in episodes.items():
                    for episode in season_episodes:
                        episode['season'] = season_num
                        self.series_episodes.append(episode)
                
                self.current_content_type = "series_episodes"
                self.content_listbox.delete(0, tk.END)
                for episode in self.series_episodes:
                    title = f"S{episode.get('season', '0')}E{episode.get('episode_num', '0')} - {episode.get('title', 'غير معروف')}"
                    self.content_listbox.insert(tk.END, title)
                
                self.content_frame.config(text=f"🎬 {series_name} ({len(self.series_episodes)})")
                self.show_category_frames("series")
                
                self.content_history.append({
                    'content_type': 'series_episodes',
                    'series_id': series_id,
                    'series_name': series_name,
                    'series_episodes': self.series_episodes,
                    'current_series_id': series_id,
                    'title': series_name
                })
                self.update_path_label()
                
        except Exception as e:
            pass

    def load_content(self, content_type):
        if not self.validate_config():
            return
            
        try:
            username = self.decrypt_data(self.server_config['username'])
            password = self.decrypt_data(self.server_config['password'])
            base_url = f"http://{self.server_config['host']}:{self.server_config['port']}"
            
            if content_type == "live":
                self.load_live_categories(base_url, username, password)
                self.content_frame.config(text="📺 البث المباشر")
                self.show_category_frames("live")
                
            elif content_type == "movies":
                self.load_movies_categories(base_url, username, password)
                self.content_frame.config(text="🎬 الأفلام")
                self.show_category_frames("movies")
                
                if not self.movies_categories:
                    self.load_all_movies(base_url, username, password)
                    
            elif content_type == "series":
                self.load_series_categories(base_url, username, password)
                self.content_frame.config(text="📺 المسلسلات")
                self.show_category_frames("series")
            
            self.content_history.append({
                'content_type': content_type,
                'series_episodes': [],
                'current_series_id': None,
                'title': {
                    'live': 'البث المباشر',
                    'movies': 'الأفلام', 
                    'series': 'المسلسلات'
                }[content_type]
            })
            self.update_path_label()
            
        except Exception as e:
            pass

    def load_all_movies(self, base_url, username, password):
        try:
            cache_key = self.get_cache_key(f"all_movies_{username}")
            movies_url = f"{base_url}/player_api.php?username={username}&password={password}&action=get_vod_streams"
            
            data = self.get_cached_data_with_fallback(movies_url, cache_key, "movies")
            if data:
                self.movies = data
                self.current_content_type = "movies"
                self.content_listbox.delete(0, tk.END)
                for movie in self.movies:
                    self.content_listbox.insert(tk.END, movie.get('name', 'غير معروف'))
                
                self.content_frame.config(text=f"🎬 جميع الأفلام ({len(self.movies)})")
                
        except Exception as e:
            pass

    def on_content_select(self, event):
        if not self.content_listbox.curselection():
            return
            
        self.current_content_index = self.content_listbox.curselection()[0]
        self.show_content_image()
        
        if self.current_content_type == "series":
            series = self.series[self.current_content_index]
            self.load_series_episodes(series.get('series_id'), series.get('name'))

    def on_content_double_click(self, event):
        if not self.content_listbox.curselection():
            return
            
        self.current_content_index = self.content_listbox.curselection()[0]
        self.play_current_content()

    def search_content(self, event=None):
        search_term = self.search_var.get().lower()
        self.content_listbox.delete(0, tk.END)
        
        if self.current_content_type == "live":
            content_list = self.channels
        elif self.current_content_type == "movies":
            content_list = self.movies
        elif self.current_content_type == "series_episodes":
            content_list = self.series_episodes
        elif self.current_content_type == "series":
            content_list = self.series
        else:
            return
        
        for item in content_list:
            name = item.get('name', '') if self.current_content_type != "series_episodes" else f"S{item.get('season', '0')}E{item.get('episode_num', '0')} - {item.get('title', '')}"
            if search_term in name.lower():
                self.content_listbox.insert(tk.END, name)

    def refresh_content(self):
        current_type = self.current_content_type
        if current_type == "live" and self.categories:
            index = self.cat_listbox.curselection()
            if index:
                category_id = self.categories[index[0]].get('category_id')
                category_name = self.categories[index[0]].get('category_name')
                self.load_live_streams(category_id, category_name)
        elif current_type == "movies" and self.movies_categories:
            index = self.movies_cat_listbox.curselection()
            if index:
                category_id = self.movies_categories[index[0]].get('category_id')
                category_name = self.movies_categories[index[0]].get('category_name')
                self.load_movies_by_category(category_id, category_name)
        elif current_type == "series" and self.series_categories:
            index = self.series_cat_listbox.curselection()
            if index:
                category_id = self.series_categories[index[0]].get('category_id')
                category_name = self.series_categories[index[0]].get('category_name')
                self.load_series(category_id, category_name)
        elif current_type == "series_episodes" and self.current_series_id:
            self.load_series_episodes(self.current_series_id, "المسلسل")

    def go_back(self):
        if len(self.content_history) > 1:
            self.content_history.pop()
            previous = self.content_history[-1]
            
            if previous['content_type'] == 'live':
                self.load_content('live')
            elif previous['content_type'] == 'movies':
                self.load_content('movies')
            elif previous['content_type'] == 'series':
                self.load_content('series')
            elif previous['content_type'] == 'series_episodes':
                series_id = previous.get('current_series_id')
                series_name = previous.get('series_name', 'المسلسل')
                if series_id:
                    self.load_series_episodes(series_id, series_name)
            
            self.update_path_label()

    def go_home(self):
        self.content_history = [{
            'content_type': 'live',
            'series_episodes': [],
            'current_series_id': None,
            'title': 'البث المباشر'
        }]
        self.load_content('live')
        self.update_path_label()

    def update_path_label(self):
        if self.content_history:
            current = self.content_history[-1]
            path_text = f"المسار: {current.get('title', 'الرئيسية')}"
            self.path_label.config(text=path_text)

    def show_vlc_settings(self):
        """إظهار إعدادات VLC المتقدمة"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("إعدادات VLC المتقدمة")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.gold_colors['dark_bg'])
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        ttk.Label(settings_window, text=f"إعدادات VLC المتقدمة - الإصدار: {self.vlc_version}", style="Title.TLabel").pack(pady=10)
        
        cache_frame = ttk.LabelFrame(settings_window, text="إعدادات الذاكرة المؤقتة", style="Custom.TFrame")
        cache_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(cache_frame, text="ذاكرة الشبكة (مللي ثانية):", style="Custom.TLabel").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        network_cache = ttk.Entry(cache_frame, style="Golden.TEntry", width=10)
        network_cache.insert(0, "5000")
        network_cache.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(cache_frame, text="ذاكرة الملفات (مللي ثانية):", style="Custom.TLabel").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        file_cache = ttk.Entry(cache_frame, style="Golden.TEntry", width=10)
        file_cache.insert(0, "5000")
        file_cache.grid(row=1, column=1, padx=5, pady=2)
        
        quality_frame = ttk.LabelFrame(settings_window, text="إعدادات الجودة والأداء", style="Custom.TFrame")
        quality_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(quality_frame, text="خيوط فك التشفير:", style="Custom.TLabel").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        threads_var = tk.StringVar(value="4")
        threads_combo = ttk.Combobox(quality_frame, textvariable=threads_var, 
                                   values=["1", "2", "4", "8", "16"], 
                                   state="readonly", style="Golden.TCombobox", width=8)
        threads_combo.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(quality_frame, text="تسريع العتاد:", style="Custom.TLabel").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        hw_var = tk.StringVar(value="any")
        hw_combo = ttk.Combobox(quality_frame, textvariable=hw_var, 
                              values=["any", "dxva2", "vaapi", "vdpau", "none"], 
                              state="readonly", style="Golden.TCombobox", width=8)
        hw_combo.grid(row=1, column=1, padx=5, pady=2)
        
        format_frame = ttk.LabelFrame(settings_window, text="التنسيقات المدعومة", style="Custom.TFrame")
        format_frame.pack(fill=tk.X, padx=10, pady=5)
        
        formats_var = tk.StringVar(value="mp4,ts,avi,mkv,flv,webm,mov,m3u8")
        formats_entry = ttk.Entry(format_frame, textvariable=formats_var, style="Golden.TEntry")
        formats_entry.pack(fill=tk.X, padx=5, pady=5)
        
        def apply_vlc_settings():
            messagebox.showinfo("نجاح", "سيتم تطبيق الإعدادات عند التشغيل التالي")
            settings_window.destroy()
        
        ttk.Button(settings_window, text="تطبيق الإعدادات", style="Golden.TButton", command=apply_vlc_settings).pack(pady=10)
        ttk.Button(settings_window, text="إغلاق", style="Golden.TButton", command=settings_window.destroy).pack(pady=5)

    def on_closing(self):
        try:
            if self.media_player.is_playing():
                self.media_player.stop()
        except:
            pass
        self.root.destroy()

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    # أولاً: عرض نافذة الدخول
    login_window = LoginWindow()
    login_result = login_window.show()
    
    # إذا تم إلغاء الدخول، إنهاء التطبيق
    if not login_result or not login_result.get('success'):
        print("تم إلغاء الدخول")
        return
    
    # ثانياً: تشغيل النافذة الرئيسية
    root = tk.Tk()
    app = AdvancedIPTVPlayer(root, login_result)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
