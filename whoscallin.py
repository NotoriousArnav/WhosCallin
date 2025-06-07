import requests
from schemas import CallerInfo

class WhosCallin:
    def __init__(self, token: str) -> None:
        self.token = f'Bearer {token}' # Tokens are Valid for 1 month
        self.headers = {
            'Authorization': self.token,
            'Accept': 'application/json'
        }

    def callerInfo(self, phonenumber: str, countryCode: str = 'in') -> CallerInfo:
        response = requests.get(
            f'https://asia-south1-truecaller-web.cloudfunctions.net/webapi/noneu/search/v2?q={phonenumber}&countryCode={countryCode}&type=44',
            headers=self.headers
        )

        if response.status_code != 200:
            raise ValueError(f"Failed to get caller info: {response.text}")

        return CallerInfo.from_dict(response.json())

    def saveToken(self, filename: str = 'trucaller.token') -> None:
        with open(filename, 'w') as file:
            file.write(self.token)

    @classmethod
    def loadToken(cls, filename: str = 'trucaller.token') -> 'WhosCallin':
        try:
            with open(filename, 'r') as file:
                token = file.read().strip()
            return cls(token)
        except FileNotFoundError:
            raise ValueError(f"Token file '{filename}' not found. Please login first.")

    @classmethod
    def login(
        cls,
        phonenumber: str,
        countryCode: str = 'in',
        input_func=input,
        verbose: bool = False,
        verboseInterrupt=lambda: input("Press Enter to Continue...")
    ) -> 'WhosCallin':
        sessionId = cls._generate_otp(phonenumber, countryCode, verbose=verbose)
        if verbose: verboseInterrupt()
        if not sessionId:
            raise ValueError("Failed to generate OTP. Please check the phone number and country code.")

        otp = input_func(f"Enter the OTP sent to {phonenumber}: ")
        token = cls._verify_otp(phonenumber, otp, sessionId, countryCode, verbose=verbose)
        if not token:
            raise ValueError("Failed to verify OTP. Please check the OTP and try again.")

        return cls(token)

    @staticmethod
    def _generate_otp(phonenumber: str, countryCode: str = 'in', verbose: bool = False) -> str:
        data = {
            'phone': int(phonenumber),
            'countryCode': countryCode,
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.truecaller.com/',
            'content-type': 'application/json',
            'Origin': 'https://www.truecaller.com'
        }

        response = requests.post(
            'https://asia-south1-truecaller-web.cloudfunctions.net/webapi/noneu/auth/truecaller/v1/send-otp',
            json=data,
            headers=headers
        )

        if verbose:
            print(f"Response: {response.content}")

        return response.json().get('sessionId')

    @staticmethod
    def _verify_otp(phonenumber: int, otp: str, sessionId: str, countryCode: str = 'in', verbose: bool = False) -> str:
        data = {
            'phone': int(phonenumber),
            'verificationCode': otp,
            'countryCode': countryCode,
            'sessionId': sessionId
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.truecaller.com/',
            'content-type': 'application/json',
            'Origin': 'https://www.truecaller.com'
        }

        response = requests.post(
            'https://asia-south1-truecaller-web.cloudfunctions.net/webapi/noneu/auth/truecaller/v1/verify-otp',
            json=data,
            headers=headers
        )

        if verbose:
            print(f"Response: {response.content}")

        return response.json().get('accessToken')
