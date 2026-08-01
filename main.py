import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64, datetime, re, socket, threading, ssl, pytz, aiohttp
from flask import Flask, request, jsonify, render_template
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say
import asyncio

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
CURRENT_TEAM_CODE = None

app = Flask(__name__, template_folder="templates", static_folder="static")

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB54"}

def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200: return (None, None)
            resp_data = await response.json(content_type=None)
            open_id = resp_data.get("open_id")
            access_token = resp_data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = "1.126.2"
    major_login.client_version_code = "2024010012"
    major_login.system_software = "Android OS 11 / API-30 (RQ3A.210805.001)"
    major_login.system_hardware = "Handheld"
    major_login.device_type = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_operator_a = "Verizon"
    major_login.network_type = "WIFI"
    major_login.network_type_a = "WIFI"
    major_login.screen_width = 1080
    major_login.screen_height = 2400
    major_login.screen_dpi = "440"
    major_login.processor_details = "ARMv8"
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.memory = 6144
    major_login.gpu_renderer = "Adreno (TM) 650"
    major_login.gpu_version = "OpenGL ES 3.2 V@1.50"
    major_login.graphics_api = "OpenGLES3"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = ""
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.login_open_id_type = 4
    major_login.access_token = access_token
    major_login.login_by = 3
    major_login.platform_sdk_id = 2
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.external_storage_total = 128512
    major_login.external_storage_available = random.randint(38000, 52000)
    major_login.internal_storage_total = 110731
    major_login.internal_storage_available = random.randint(18000, 32000)
    major_login.game_disk_storage_total = 26628
    major_login.game_disk_storage_available = random.randint(18000, 25000)
    major_login.external_sdcard_total_storage = 119234
    major_login.external_sdcard_avail_storage = random.randint(25000, 60000)
    major_login.library_path = "/data/app/~~random/base.apk"
    major_login.library_token = "hash|base.apk"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.supported_astc_bitset = 16383
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = random.randint(9000, 18000)
    major_login.release_channel = "android"
    major_login.channel_type = 3
    major_login.reg_avatar = 1
    major_login.if_push = 1
    major_login.is_vpn = 0
    major_login.android_engine_init_flag = 110009
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggpolarbear.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'

async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT:
        if whisper_writer is None: return 'Chat writer not connected'
        whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine':
        if online_writer is None: return 'Online writer not connected'
        online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)'

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.1):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave
    consecutive_fails = 0
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            consecutive_fails = 0  # reset on successful connect
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: break

                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)

                        message = f'[B][C]{get_random_color()}\n- WeLComE To Emote Bot ! '
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                    except:
                        pass

            # Server closed the connection — clean up
            try:
                online_writer.close()
                await online_writer.wait_closed()
            except:
                pass
            online_writer = None

        except Exception as e:
            print(f"- ErroR OnLine {ip}:{port} - {e}")
            online_writer = None
            consecutive_fails += 1
            # After 3 straight failures the token is dead — bubble up so
            # StarTinG can do a full re-login
            if consecutive_fails >= 3:
                raise Exception(f"OnLine reconnect failed {consecutive_fails}x — triggering re-login")

        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break

                if data.hex().startswith("120000"):
                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None

                    if response:
                        if inPuTMsG.startswith(("/5")):
                            try:
                                message = f"[B][C]{get_random_color()}\n\nAccepT My InV FasT\n\n"
                                P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                                PAc = await OpEnSq(key , iv,region)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , PAc)
                                C = await cHSq(5, uid ,key, iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , C)
                                V = await SEnd_InV(5 , uid , key , iv,region)
                                await asyncio.sleep(0.5)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , V)
                                E = await ExiT(None , key , iv)
                                await asyncio.sleep(3)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , E)
                            except:
                                pass

                        if inPuTMsG.startswith('/x/'):
                            CodE = inPuTMsG.split('/x/')[1]
                            try:
                                EM = await GenJoinSquadsPacket(CodE , key , iv)
                                await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                            except:
                                pass

                        if inPuTMsG.startswith('leave'):
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)

                        if inPuTMsG.strip().startswith('/s'):
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)

                        if inPuTMsG.strip().startswith('/f'):
                                parts = inPuTMsG.strip().split()
                                message = f'[B][C]{get_random_color()}\nACITVE TarGeT -> {xMsGFixinG(uid)}\n'
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                uid2 = uid3 = uid4 = uid5 = uid6 = None
                                s = False
                                try:
                                    uid = int(parts[1])
                                    uid2 = int(parts[2])
                                    uid3 = int(parts[3])
                                    uid4 = int(parts[4])
                                    uid5 = int(parts[5])
                                    uid6 = int(parts[6])
                                    idT = int(parts[6])
                                except:
                                    s = True
                                if not s:
                                    try:
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        for i in range(200):
                                            H = await Emote_k(uid, idT, key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                            if uid2:
                                                H = await Emote_k(uid2, idT, key, iv, region)
                                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                            await asyncio.sleep(0.08)
                                    except:
                                        pass

                        if inPuTMsG in ("dev"):
                            message = '/d <uid1>... <emoteid> /f <uid1>... <emoteid> for fast emote'
                            P = await SEndMsG(response.Data.chat_type , message , uid , chat_id , key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)
                        response = None
            whisper_writer.close() ; await whisper_writer.wait_closed() ; whisper_writer = None
        except Exception as e: print(f"ErroR {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

import glob as _glob

def _build_emote_data():
    emotes = {}
    categories = {"All": [], "Old": [], "New": [], "Evo": [], "Rare": []}
    emote_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "emotes")

    # Load real emote names from database
    _name_db = {}
    _name_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "emote_names.json")
    if os.path.exists(_name_db_path):
        with open(_name_db_path, 'r') as _f:
            _name_db = json.load(_f)

    # Evo Gun emote IDs — explicit list (span multiple ID ranges so can't
    # rely on numeric range alone)
    _EVO_IDS = {
        909000063,  # AK47     – Blue Flame Draco    → Draco's Soul
        909000068,  # SCAR     – Megalodon Alpha      → Megalodon Attack
        909000071,  # MP40     – Predatory Cobra      → Cobra Dance
        909000081,  # M1014    – Green Flame Draco    → Dragon Splash
        909000085,  # XM8      – Destiny Guardian     → Lightning Strike
        909000090,  # FAMAS    – Demonic Grin         → Demon's Roar
        909000098,  # UMP      – Booyah Day 2021      → Booyah Power
        909033001,  # M4A1     – Infernal Draco       → Infernal Burst
        909033002,  # MP5      – Platinum Divinity    → Angelic Grace
        909034001,  # Rampage  – Hyperbook            → Book Power
        909035007,  # M1887    – Sterling Conqueror   → Conqueror's Slash
        909035010,  # G36      – Violet Threat        → Purple Phantom
        909035012,  # AN94     – Evil Howler          → Howler's Rage
        909037011,  # Evo Fist – Bonebreaker          → Flaming Punch
        909038010,  # Thompson – Cindered Colossus    → Fire Surge
        909038012,  # G18      – Lethal Fangs         → Serpent Bite
        909039011,  # M1014 2.0– Scorpio Shatter      → Scorpio Sting
        909040010,  # Vector   – Chromasonic          → Sonic Wave
        909041005,  # Groza    – Bang Pop             → Cyber Blast
        909042008,  # Woodpecker– Majestic Prowler    → Panther Pounce
        909049010,  # P90      – Marvelous Zenith     → Cosmic Zenith
        909051003,  # M60      – Cosmic Volcano       → Lava Eruption
    }

    # Track duplicate names to ensure unique keys
    _name_count = {}
    for path in sorted(_glob.glob(os.path.join(emote_dir, "*.png"))):
        fname = os.path.basename(path)
        emote_id = int(fname.replace(".png", ""))
        raw_name = _name_db.get(str(emote_id), f"Emote {emote_id}")
        # Make name unique if duplicated
        if raw_name in _name_count:
            _name_count[raw_name] += 1
            name = f"{raw_name} ({_name_count[raw_name]})"
        else:
            _name_count[raw_name] = 1
            name = raw_name

        emotes[name] = emote_id
        categories["All"].append(name)

        # Evo IDs take priority over range-based bucket
        if emote_id in _EVO_IDS:
            categories["Evo"].append(name)
        elif emote_id <= 909009999:
            categories["Old"].append(name)
        elif emote_id <= 909039999:
            categories["Rare"].append(name)
        elif emote_id <= 909046999:
            categories["Evo"].append(name)
        else:
            categories["New"].append(name)
    return emotes, categories

_EMOTES, _CATEGORIES = _build_emote_data()

REGIONS_LIST = [
    {"code": "bd",  "label": "Bangladesh",       "has_bot": True},
    {"code": "ind", "label": "India",            "has_bot": False},
    {"code": "np",  "label": "Nepal",            "has_bot": False},
    {"code": "sg",  "label": "Singapore/Global", "has_bot": False},
    {"code": "us",  "label": "United States",    "has_bot": False},
    {"code": "br",  "label": "Brazil",           "has_bot": False},
    {"code": "id",  "label": "Indonesia",        "has_bot": False},
    {"code": "tw",  "label": "Taiwan",           "has_bot": False},
    {"code": "th",  "label": "Thailand",         "has_bot": False},
    {"code": "vn",  "label": "Vietnam",          "has_bot": False},
    {"code": "me",  "label": "Middle East",      "has_bot": False},
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health')
def api_health():
    return jsonify({"status": "ok", "bot_online": online_writer is not None})

@app.route('/api/regions')
def api_regions():
    return jsonify({"regions": REGIONS_LIST})

@app.route('/api/emotes')
def api_emotes():
    return jsonify({
        "emotes":     _EMOTES,
        "categories": _CATEGORIES,
        "total":      len(_EMOTES),
    })

@app.route('/api/send', methods=['POST'])
def api_send():
    global loop
    data      = request.get_json(force=True) or {}
    uids      = data.get('uids', [])
    team_code = data.get('team_code', '')
    emote_name= data.get('emote_name', '')
    count     = int(data.get('count', 1))

    if not uids or not team_code or not emote_name:
        return jsonify({"message": "Missing uids, team_code or emote_name"}), 400

    emote_id = _EMOTES.get(emote_name)
    if emote_id is None:
        return jsonify({"message": f"Unknown emote: {emote_name}"}), 400

    # Do NOT short-circuit here — perform_emote will wait up to 10s for
    # the connection to come back (it drops briefly after each squad-join
    # packet while TcPOnLine reconnects).
    results = []
    for uid in uids:
        try:
            fut = asyncio.run_coroutine_threadsafe(
                perform_emote(team_code, [uid], emote_id), loop
            )
            fut.result(timeout=15)
            results.append({"uid": uid, "success": True,  "message": "Emote sent!"})
        except Exception as e:
            results.append({"uid": uid, "success": False, "message": str(e)})

    return jsonify({"results": results})

loop = None
_emote_lock = None

async def _get_emote_lock():
    global _emote_lock
    if _emote_lock is None:
        _emote_lock = asyncio.Lock()
    return _emote_lock

async def _wait_for_writer(timeout=10):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if online_writer is not None:
            return True
        await asyncio.sleep(0.2)
    return False

async def perform_emote(team_code: str, uids: list, emote_id: int):
    global key, iv, region, online_writer, BOT_UID, CURRENT_TEAM_CODE

    # ── Step 1: Wait for connection BEFORE acquiring the lock ──────────────
    # After each squad-join packet the FF server drops the TCP connection;
    # TcPOnLine reconnects in ~0.1-0.3 s.  Waiting here (without the lock)
    # lets multiple concurrent requests share the wait instead of blocking
    # each other serially.
    ready = await _wait_for_writer(timeout=10)
    if not ready:
        raise Exception("Bot not connected to game server. Please try again.")

    # ── Step 2: Acquire lock only for the actual packet write ──────────────
    lock = await _get_emote_lock()
    async with lock:
        # Re-check: connection may have dropped while we waited for the lock
        if online_writer is None:
            raise Exception("Connection lost. Please try again.")

        try:
            # 1) Join squad
            EM = await GenJoinSquadsPacket(team_code, key, iv)
            online_writer.write(EM)
            await online_writer.drain()

            # 2) Short pause — lets the server process the join before the
            #    emote packet arrives.  The TCP connection will drop right
            #    after drain() (server behaviour); TcPOnLine will reconnect
            #    automatically.  We don't need the connection alive past here.
            await asyncio.sleep(0.1)

            # 3) Re-grab the writer — it may have been replaced by reconnect
            w = online_writer
            if w is None:
                # Wait briefly for reconnect
                ready2 = await _wait_for_writer(timeout=5)
                if not ready2:
                    raise Exception("Reconnect timed out after join")
                w = online_writer

            # 4) Send emote packets for each UID
            for uid_str in uids:
                pkt = await Emote_k(int(uid_str), emote_id, key, iv, region)
                w.write(pkt)
            await w.drain()

            CURRENT_TEAM_CODE = None
            return {"status": "success", "message": "Emote sent"}

        except Exception as e:
            raise Exception(f"Emote failed: {str(e)}")


@app.route('/join')
def join_team():
    global loop
    team_code = request.args.get('tc')
    uid1 = request.args.get('uid1')
    uid2 = request.args.get('uid2')
    uid3 = request.args.get('uid3')
    uid4 = request.args.get('uid4')
    uid5 = request.args.get('uid5')
    uid6 = request.args.get('uid6')
    emote_id_str = request.args.get('emote_id')

    if not team_code or not emote_id_str:
        return jsonify({"status": "error", "message": "Missing tc or emote_id"})

    try:
        emote_id = int(emote_id_str)
    except:
        return jsonify({"status": "error", "message": "emote_id must be integer"})

    uids = [uid for uid in [uid1, uid2, uid3, uid4, uid5, uid6] if uid]

    if not uids:
        return jsonify({"status": "error", "message": "Provide at least one UID"})

    asyncio.run_coroutine_threadsafe(
        perform_emote(team_code, uids, emote_id), loop
    )

    return jsonify({
        "status": "success",
        "team_code": team_code,
        "uids": uids,
        "emote_id": emote_id_str,
        "message": "Emote triggered"
    })


async def MaiiiinE():
    global loop, key, iv, region, BOT_UID

    BOT_UID = int('16198983266')
    Uid, Pw = '4729988582', 'B2CCC0B2DA03994D06106ECA4AB491DB33313F99ABEC19D4E0249416041952D2'

    open_id, access_token = await GeNeRaTeAccEss(Uid, Pw)
    if not open_id or not access_token:
        print("ErroR - InvaLid AccounT")
        return None

    PyL = await EncRypTMajoRLoGin(open_id, access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE:
        print("TarGeT AccounT => BannEd / NoT ReGisTeReD !")
        return None

    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    region = MajoRLoGinauTh.region
    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp

    loop = asyncio.get_running_loop()

    LoGinDaTa = await GetLoginData(UrL, PyL, ToKen)
    if not LoGinDaTa: return None

    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP, OnLineporT = OnLinePorTs.split(":")
    ChaTiP, ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    equie_emote(ToKen, UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT), ToKen, int(timestamp), key, iv)
    ready_event = asyncio.Event()

    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region))
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP, OnLineporT, key, iv, AutHToKen))

    os.system('clear')
    R  = '\033[91m'
    G  = '\033[92m'
    Y  = '\033[93m'
    C  = '\033[96m'
    W  = '\033[97m'
    DIM= '\033[2m'
    B  = '\033[1m'
    RS = '\033[0m'
    print(f"{C}{B}")
    print("   ░█▀▀▀█ ▀█▀ ░█▀▀▀ ─█▀▀█ ▀▀█▀▀")
    print("   ─▀▀▀▄▄ ░█─ ░█▀▀▀ ░█▄▄█ ─░█──")
    print(f"   ░█▄▄▄█ ▄█▄ ░█─── ░█─░█ ─░█──{RS}")
    print(f"\n   {DIM}{W}{'─' * 44}{RS}")
    print(f"   {DIM}{W}  Author{RS} {W}{B}: SIFAT{RS}   {DIM}{W}│{RS}   {DIM}{W}FF Emote Bot{RS}")
    print(f"   {DIM}{W}{'─' * 44}{RS}\n")
    print(f"   {W}┌{'─' * 38}┐{RS}")
    print(f"   {W}│{RS}")
    print(f"   {W}│{RS}   {Y}{B}TARGET UID  {W}──►{RS}  {G}{B}{TarGeT}{RS}")
    print(f"   {W}│{RS}   {Y}{B}BOT NAME    {W}──►{RS}  {C}{B}{acc_name}{RS}")
    print(f"   {W}│{RS}   {Y}{B}STATUS      {W}──►{RS}  {G}{B}ONLINE  ✔{RS}")
    print(f"   {W}│{RS}   {Y}{B}REGION      {W}──►{RS}  {C}{B}{region.upper()}{RS}")
    print(f"   {W}│{RS}")
    print(f"   {W}└{'─' * 38}┘{RS}\n")

    await asyncio.gather(task1, task2)


async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE(), timeout=7 * 60 * 60)
        except asyncio.TimeoutError:
            print("Token ExpiRed ! , ResTartinG")
        except Exception as e:
            print(f"ErroR TcP - {e} => ResTarTinG ...")

if __name__ == '__main__':
    bot_thread = threading.Thread(target=lambda: asyncio.run(StarTinG()), daemon=True)
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
