"""
# WhosCallin - A Python wrapper for Truecaller API to fetch caller information.
This module provides a class `WhosCallin` to interact with the Truecaller API,
allowing users to login with their phone number and OTP, retrieve caller information,
and manage authentication tokens. It includes methods for generating and verifying OTPs,
and saving/loading authentication tokens from a file.
"""
import requests
from whoscallin.schemas import CallerInfo

class WhosCallin:
    """
    A class to interact with the Truecaller API for caller information.
    This class allows you to login using a phone number and OTP, retrieve caller information,
    and save/load the authentication token.
    Attributes:
        token (str): The authentication token for Truecaller API.
        headers (dict): Headers to be used in API requests.
    Methods:
        callerInfo(phonenumber: str, countryCode: str = 'in') -> CallerInfo:
            Retrieves caller information for a given phone number.
        saveToken(filename: str = 'trucaller.token') -> None:
            Saves the authentication token to a file.
        loadToken(filename: str = 'trucaller.token') -> 'WhosCallin':
            Loads the authentication token from a file.
        login(phonenumber: str, countryCode: str = 'in', input_func=input, verbose: bool = False, verboseInterrupt=lambda: input("Press Enter to Continue...")) -> 'WhosCallin':
            Logs in to Truecaller using phone number and OTP.
        _generate_otp(phonenumber: str, countryCode: str = 'in', verbose: bool = False) -> str:
            Generates an OTP for the given phone number.
        _verify_otp(phonenumber: int, otp: str, sessionId: str, countryCode: str = 'in', verbose: bool = False) -> str:
            Verifies the OTP and returns the authentication token.
    """
    def __init__(self, token: str) -> None:
        self.token = f'Bearer {token}' # Tokens are Valid for 1 month
        self.headers = {
            'Authorization': self.token,
            'Accept': 'application/json'
        }

    def callerInfo(self, phonenumber: str, countryCode: str = 'in') -> CallerInfo:
        """
        Retrieves caller information for a given phone number.
        Args:
            phonenumber (str): The phone number to search for.
            countryCode (str): The country code for the phone number (default is 'in' for India).
        Returns:
            CallerInfo: An instance of CallerInfo containing the caller details.
        Raises:
            ValueError: If the API request fails or returns an error.
        """
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
        """
        Logs in to Truecaller using phone number and OTP.
        Args:
            phonenumber (str): The phone number to login with.
            countryCode (str): The country code for the phone number (default is 'in' for India).
            input_func (callable): Function to get user input (default is built-in input).
            verbose (bool): If True, prints additional information during the process.
            verboseInterrupt (callable): Function to interrupt and wait for user input in verbose mode.
        Returns:
            WhosCallin: An instance of WhosCallin with the authentication token.
        Raises:
            ValueError: If the OTP generation or verification fails.
        """
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
    def _generate_otp(
            phonenumber: str,
            countryCode: str = 'in',
            verbose: bool = False
        ) -> str:
        """
        Generates an OTP for the given phone number.
        Args:
            phonenumber (str): The phone number to generate OTP for.
            countryCode (str): The country code for the phone number (default is 'in' for India).
            verbose (bool): If True, prints additional information during the process.
        Returns:
            str: The session ID if OTP generation is successful, None otherwise.
        """
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

        return response.json().get('sessionId', None)

    @staticmethod
    def _verify_otp(
            phonenumber: int,
            otp: str,
            sessionId: str,
            countryCode: str = 'in',
            verbose: bool = False
        ) -> str:
        """
        Verifies the OTP and returns the authentication token.
        Args:
            phonenumber (int): The phone number to verify.
            otp (str): The OTP received by the user.
            sessionId (str): The session ID generated during OTP generation.
            countryCode (str): The country code for the phone number (default is 'in' for India).
            verbose (bool): If True, prints additional information during the process.
        Returns:
            str: The authentication token if verification is successful.
        """
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

        return response.json().get('accessToken', None) # These are valid for 1 month
