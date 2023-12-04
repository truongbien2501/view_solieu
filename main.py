from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen,CardTransition,SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton,MDFlatButton,MDRaisedButton,MDFloatingActionButtonSpeedDial
from kivy_garden.mapview import MapView,MarkerMapLayer,MapMarkerPopup
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase
from kivy.utils import get_color_from_hex
from kivymd.icon_definitions import md_icons
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.list import OneLineAvatarListItem, ImageLeftWidget
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior, CircularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.swiper import MDSwiper
from kivy.uix.behaviors import ButtonBehavior
import numpy as np
import requests
from datetime import datetime,timedelta
import io
from PIL import Image as PILImage
from ftplib import FTP
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineListItem,OneLineIconListItem,IconLeftWidget
from kivy.metrics import dp
from kivymd.icon_definitions import md_icons
from kivymd.uix.gridlayout import MDGridLayout

# Window.size = (350, 600)

class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''

class Homescreen(ScreenManager):
    def login(self,username, password):
        # print('da click')
        # Thực hiện xác thực đăng nhập ở đây (ví dụ: kiểm tra tên đăng nhập và mật khẩu)
        if username == 'admin' and password == 'ttb':
            app = MDApp.get_running_app()
            app.root.current = 'trangchu'  # Chuyển đến màn hình chính
        else:
            # self.show_error_dialog()
            self.thongbao()

    def thongbao(self):
        toast("Không đúng tên hoặc mật khẩu")
        
class RectangularRippleButton(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    pass


class RectangularRippleImage(CircularRippleBehavior, ButtonBehavior, Image):
    pass


class SOLIEU_KTTV(MDApp):
    def build(self):
        self.title = "KTTV TTB"
        self.theme_cls.primary_palette = "Pink"
        Builder.load_file('main.kv')
        self.scr = Homescreen()
        self.scr.current = 'trangchu'
        # self.scr.ids.bottom_navigation.switch_tab('chart')
        return self.scr

    def on_start(self):
        tinh = ['Quang Ngai','Quang Nam','Da Nang', 'Thua Thien Hue','Quang Tri','Quang Binh']
        # tạo các icon
        for tram in tinh:
            icon_item = OneLineIconListItem(
                IconLeftWidget(icon="weather-partly-rainy"),
                text=tram,
                on_release=self.icon_pressed
            )
            # gán su kien cho icon
            self.root.ids.provin.add_widget(icon_item)

    
    def icon_pressed(self,instance): # su kien click vao cac o tỉnh
        clicked_text = instance.text
        # print(clicked_text)
        app = MDApp.get_running_app()
        app.root.current = 'solieu'
        self.root.ids.tramkttv_tinh.clear_widgets()
        self.root.ids.tieude_solieu.title = clicked_text
        self.root.ids.hintexx.hint_text = "Tìm kiếm:" + clicked_text
        ds_tram = np.genfromtxt('TTB.txt', delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
            if str(tram[4]) == str(clicked_text):
                print(tram[4])
                icon_item = OneLineIconListItem(
                    IconLeftWidget(icon="weather-partly-rainy"),
                    text=tram[1] + ' - ' + tram[3],
                    on_release=self.tram_pressed
                )
                # gán su kien cho icon
                self.root.ids.tramkttv_tinh.add_widget(icon_item)
                
    def search_tram(self, search_text):# su kien tìm kiếm
        self.root.ids.tramkttv_tinh.clear_widgets()
        # self.root.ids.hintexx.helper_text = self.root.ids.tieude_solieu.title
        ds_tram = np.genfromtxt('TTB.txt', delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
            if str(tram[1]) == str(search_text):
                icon_item = OneLineIconListItem(
                    IconLeftWidget(icon="weather-partly-rainy"),
                    text=tram[1] + ' - ' + tram[3],
                    on_release=self.tram_pressed
                )
                # gán su kien cho icon
                self.root.ids.tramkttv_tinh.add_widget(icon_item)
    
    def tram_pressed(self,instance): # su kien click vao tram
        clicked_text = instance.text
        app = MDApp.get_running_app()
        app.root.current = 'tram'
        self.root.ids.solieutram.clear_widgets()
        self.root.ids.tieude_tram.title = clicked_text
        tt_tram = clicked_text.split('-')
        tentram = str(tt_tram[0]).strip()
        yeuto = str(tt_tram[1]).strip()
        ds_tram = np.genfromtxt('TTB.txt', delimiter=',', dtype=None, names=True, encoding=None)
        for tram in ds_tram:
            # print(str(tram[1]))
            # print(str(tram[3]))
            # print(str(tentram))
            # print(str(yeuto))
            if str(tram[1]) == str(tentram) and str(tram[3]) == str(yeuto):
                solieu = self.TTB_API(tram[0],tram[2])
                # print(solieu)
                for value in range(len(solieu) - 1, -1, -1):
                    icon_item = OneLineIconListItem(
                        text=solieu[value]['Thoigian_SL'] + ' : ' + solieu[value]['Solieu']
                    )
                    # gán su kien cho icon
                    self.root.ids.solieutram.add_widget(icon_item)
                break
    
    
    
    def callback_trangchu(self):
        app = MDApp.get_running_app()
        app.root.current = 'trangchu'
        
    def callback_solieu(self):
        app = MDApp.get_running_app()
        app.root.current = 'solieu'
    # def callback_solieu(self):
    #     app = MDApp.get_running_app()
    #     app.root.current = 'solieu'
        
        
        
    def callback_for_menu_items(self, *args):
        toast(args[0])

    def show_example_grid_bottom_sheet(self):
        # pass
        bottom_sheet_menu = MDGridBottomSheet()
        data = {
            "Mực nước": "waves-arrow-up",
            "Q đến": "alpha-q-circle",
            "Q xả": "alpha-d-circle-outline",
            "Mưa": "weather-pouring",
            "Mưa tại đập": "alpha-c-circle-outline",
        }
        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0],
                lambda x, y=item[0]: self.callback_for_menu_items(y),
                icon_src=item[1],
            )
        bottom_sheet_menu.open()
    
    def callback_for_menu_items(self, selected_item):
        # Thực hiện cập nhật hình ảnh dựa trên mục được chọn
        if selected_item == "Mực nước":
            self.read_ftp_sever_image('chart_H.png')
            self.root.ids.image_chart_td.source = 'cache/chart_H.png'
        elif selected_item == "Q đến":
            self.read_ftp_sever_image('chart_Q.png')
            self.root.ids.image_chart_td.source = 'cache/chart_Q.png'
        elif selected_item == "Q xả":
            self.read_ftp_sever_image('chart_Q_xa.png')
            self.root.ids.image_chart_td.source = 'cache/chart_Q_xa.png'
        elif selected_item == "Mưa":
            self.read_ftp_sever_image('chart_mua_tranam2.png')
            self.root.ids.image_chart_td.source = 'cache/chart_mua_tranam2.png'
        elif selected_item == "Mưa tại đập":
            self.read_ftp_sever_image('chart_mua_tramdapst2.png')
            self.root.ids.image_chart_td.source = 'cache/chart_mua_tramdapst2.png'
    
    def show_marker_info(self,tram,thongtin):
        toast(tram + ':' + thongtin)

        
    def TTB_API_HC(self):
        now = datetime.now()
        kt = datetime(now.year,now.month,now.day,now.hour)
        bd = kt - timedelta(days=1)
        # data = pd.DataFrame()
        # data['time'] = pd.date_range(bd,kt,freq='T')
        matram = '5ST'
        # muc nuoc
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=1&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,'ho_dakdrinh_mucnuoc',bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        response = requests.get(pth)
        mucnuoc = np.array(response.json())
        # mua
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=1&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,'ho_dakdrinh_qve',bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        response = requests.get(pth)
        mua = np.array(response.json())
        return mucnuoc,mua
    
    def tinhmua(self,data,bd,kt):
        tonngmua = 0
        for a in range(data.shape[0]-1,1,-1):
            date_object = datetime.strptime(data[a]['Thoigian_SL'], "%Y-%m-%d %H:%M:%S")
            if date_object > bd and date_object <=kt:
                tonngmua+= float(data[a]['Solieu'])
        return tonngmua
    
    
    def TTB_API(self,matram,ten_bang):
        now = datetime.now()
        kt = datetime(now.year,now.month,now.day,now.hour)
        bd = kt - timedelta(days=1)
        # mua
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=60&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,ten_bang,bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        print(pth)
        response = requests.get(pth)
        mua = np.array(response.json())
        print(mua)
        # if len(mua) < 5:
        #     return '-','-'
        return mua
    
    def TTB_API_SONGTRANH_muatong(self,matram):
        now = datetime.now()
        kt = datetime(now.year,now.month,now.day,now.hour)
        bd = kt - timedelta(days=1)
        # mua
        pth = 'http://113.160.225.84:2018/API_TTB/JSON/solieu.php?matram={}&ten_table={}&sophut=1&tinhtong=0&thoigianbd=%27{}%2000:00:00%27&thoigiankt=%27{}%2023:59:00%27'
        pth = pth.format(matram,'mua_songtranh',bd.strftime('%Y-%m-%d'),kt.strftime('%Y-%m-%d'))
        response = requests.get(pth)
        mua = np.array(response.json())
        if len(mua) < 5:
            return '-','-','-','-','-','-'
        else:
            giohientai = datetime.strptime(mua[-1]['Thoigian_SL'], '%Y-%m-%d %H:%M:%S')
            mua1 = self.tinhmua(mua,giohientai-timedelta(hours=1),giohientai)
            mua1 = '{:.2f}'.format(mua1)
            mua3 = self.tinhmua(mua,giohientai-timedelta(hours=3),giohientai)
            mua3 = '{:.2f}'.format(mua3)
            mua6 = self.tinhmua(mua,giohientai-timedelta(hours=6),giohientai)
            mua6 = '{:.2f}'.format(mua6)
            mua12 = self.tinhmua(mua,giohientai-timedelta(hours=12),giohientai)
            mua12 = '{:.2f}'.format(mua12)
            mua24 = self.tinhmua(mua,giohientai-timedelta(hours=24),giohientai)
            mua24 = '{:.2f}'.format(mua24)
        return mua1,mua3,mua6,mua12,mua24, mua[-1]['Thoigian_SL']
    
    
    def read_ftp_sever_image(self,tenanh):
        # Thông tin máy chủ FTP và đường dẫn đến file ftp://203.209.181.174/DAKDRINH/Image
        ftp_host = '203.209.181.174'
        ftp_user = 'admin'
        ftp_password = 'Supportdng'
        file_path = 'SONGTRANH/Image' + '/' + tenanh
        # Kết nối đến máy chủ FTP
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_password)
        with open('cache/'+ tenanh, 'wb') as local_file:
            ftp.retrbinary('RETR ' + file_path, local_file.write)
        ftp.quit()
        
    
    def get_ftp_image(self,tram):
        self.read_ftp_sever_image(tram)
        self.root.ids.image_chart_tvhn.source = "cache/" + tram


    def get_custom_value(self):
        mucnuoc,qve = self.TTB_API_HC()
        # Trả về giá trị bạn muốn
        return mucnuoc[-1]['Solieu'],qve[-1]['Solieu']


if __name__ == '__main__':
    SOLIEU_KTTV().run()
