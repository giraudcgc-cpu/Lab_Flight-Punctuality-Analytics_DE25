USE ROLE USERADMIN;

CREATE USER IF NOT EXISTS flight_reporter_user
    TYPE = SERVICE
    RSA_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAj71vK5Jf8xodJlLiDH//Dri1D4Zm7UcT6f/mMSOgRAbmbqhH6sRC9poZvWN7QaCxIQpbTfwaW9Ih4bUPhnHohu08lQjKh/HVxYTYVcbKoJzG8w4c0mbNvQutDgSjQoeRqjAoUBoi55WJymjEvJ7KyzgsiUIw+3LuCXQaTCfpzilqiR9MZBU/2k3Tz/PSBUNjPe6EuWF0xMjOfFM3g8G4IJGz78/5b/0dcmlYsN3v+Y8tmAYSf3J7KidfxONGL8UQo76+SjL79kbKFZ+/dPrLUKizSpdBm3Ip8sAyFpBZli6zDP+599SvWS+9k0ixpVXeo+fYTIz120XFnPWIDCnxFQIDAQAB'
    DEFAULT_ROLE = flight_reporter_role
    DEFAULT_WAREHOUSE = flight_wh
    DEFAULT_NAMESPACE = 'flight_punctuality.marts'
    COMMENT = 'Service user for the streamlit dashboard (read only)';

-- check: RSA_PUBLIC_KEY_FP should have a value
DESC USER flight_reporter_user;