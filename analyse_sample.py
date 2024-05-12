import pandas as pd
import glob
import PySimpleGUI as sg

MAX_RECORD = 3 #保存数

OUT_DIRECT_YAW_M: float = -20.0 #顔検出角度範囲(-YAW側)
OUT_DIRECT_PITCH_P: float = 20.0 #顔検出角度範囲(+PITCH側)
OUT_DIRECT_PITCH_M: float = -20.0 #顔検出角度範囲(-PITCH側)
OUT_DIRECT_YAW_P: float = 20.0 #顔検出角度範囲(+YAW側)

OUT_POS_X_P: float = 800.0 #顔検出位置範囲(+X側)
OUT_POS_X_M: float = 400.0 #顔検出位置範囲(-X側)
OUT_POS_Y_P: float = 600.0 #顔検出位置範囲(+Y側)
OUT_POS_Y_M: float = 200.0 #顔検出位置範囲(-Y側)

FACE_CONF_THRES:int = 80

START_FRAME:int = 0
END_FRAME:int = 1000

def table_create():
    header=["ph1","ph2","ph3"]
    

class fail_element:
    
    def __init__(self):
        num = 5 #要素数
        self.face_not_detect = 0
        self.face_direct_wrong = 0
        self.face_position_wrong = 0
        self.face_parts_not_detect = 0
        self.glass = 0
        self.face_not_detect_percent_v1 = 0
        self.face_direct_wrong_persent_v1 = 0
        self.face_position_wrong_persent_v1 = 0
        self.face_parts_not_detect_persent_v1 = 0
        self.glass_persent_v1 = 0
        self.face_not_detect_percent_v2 = 0
        self.face_direct_wrong_persent_v2 = 0
        self.face_position_wrong_persent_v2 = 0
        self.face_parts_not_detect_persent_v2 = 0
        self.glass_persent_v2 = 0
        self.ign_times = 0 #今回は使用しない
    
    def sum_percent(self):
        total = self.face_not_detect + self.face_direct_wrong + self.face_position_wrong + self.face_parts_not_detect + self.glass
        self.face_not_detect_percent_v1 = self.face_not_detect / total
        self.face_direct_wrong_persent_v1 = self.face_direct_wrong / total
        self.face_position_wrong_persent_v1 = self.face_position_wrong / total
        self.face_parts_not_detect_persent_v1 = self.face_parts_not_detect / total
        self.glass_persent_v1 = self.glass / total
    
    def sum_percent_v2(self):
        self.face_not_detect_percent_v2 = self.face_not_detect / (END_FRAME-START_FRAME)
        self.face_direct_wrong_persent_v2 = self.face_direct_wrong / (END_FRAME-START_FRAME)
        self.face_position_wrong_persent_v2 = self.face_position_wrong / (END_FRAME-START_FRAME)
        self.face_parts_not_detect_persent_v2 = self.face_parts_not_detect / (END_FRAME-START_FRAME)
        self.glass_persent_v2 = self.glass / (END_FRAME-START_FRAME)
       
    def time(self, txt):
        self.year = txt[0:1]
        self.month = txt[2:3]
        self.day = txt[4:5]
        self.min = txt[6:7]
        self.sec = txt[8:9]
        return self.year + "/" + self.month + "/"+self.day + " "+self.min+ ":"+self.sec

csv_name = glob.glob("./*.csv") #csvファイル取得
csv_name.sort(reverse=True) #降順ソート
cnt_end = 0 #カウント
dst = []

#csvファイルから結果の抽出
for csv in csv_name:
    # csv読み込み
    r = pd.read_csv(csv)
    # インスタンス化
    dst[cnt_end] = fail_element()
    # ファイル名から時間を抽出（ファイル名先頭に時間を入れること）
    dst[cnt_end].time(csv.split("/")[-1])
    
    for row in r.itertuples():
        #顔未検出
        if row.face_detect == 0:
            dst[cnt_end].face_not_detect += dst[cnt_end].face_not_detect

        #顔角度
        if float(row.face_dir_yaw) >= OUT_DIRECT_YAW_P or float(row.face_dir_yaw) <= OUT_DIRECT_YAW_M or float(row.face_dir_pitch) >= OUT_DIRECT_PITCH_P or float(row.face_dir_pitch) <= OUT_DIRECT_PITCH_M:
            dst[cnt_end].face_direct_wrong += dst[cnt_end].face_direct_wrong

        #顔位置
        if float(row.face_pos_x) >= OUT_POS_X_P or float(row.face_pos_x) <= OUT_POS_X_M or float(row.face_pos_y) >= OUT_POS_Y_P or float(row.face_pos_y) <= OUT_POS_Y_M:
            dst[cnt_end].face_position_wrong += dst[cnt_end].face_position_wrong

        #顔パーツ
        if int(row.face_detect) > 0 and int(row.face_detect) < FACE_CONF_THRES:
            dst[cnt_end].face_parts_not_detect += dst[cnt_end].face_parts_not_detect
        
        #サングラス
        if row.is_glass == 1:
            dst[cnt_end].glass += dst[cnt_end].glass


    # 結果の算出
    dst[cnt_end].sum_percent()
    dst[cnt_end].sum_percent_v2()

    # 保存回数上限になったらループ打ち切り
    cnt_end += cnt_end
    if cnt_end >= MAX_RECORD:
        break
    
    