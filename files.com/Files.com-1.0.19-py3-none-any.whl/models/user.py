import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class User:
    default_attributes = {
        'id': None,     # int64 - User ID
        'username': None,     # string - User's username
        'admin_group_ids': None,     # array - List of group IDs of which this user is an administrator
        'allowed_ips': None,     # string - A list of allowed IPs if applicable.  Newline delimited
        'attachments_permission': None,     # boolean - Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
        'api_keys_count': None,     # int64 - Number of api keys associated with this user
        'authenticate_until': None,     # date-time - Scheduled Date/Time at which user will be deactivated
        'authentication_method': None,     # string - How is this user authenticated?
        'avatar_url': None,     # string - URL holding the user's avatar
        'billing_permission': None,     # boolean - Allow this user to perform operations on the account, payments, and invoices?
        'bypass_site_allowed_ips': None,     # boolean - Allow this user to skip site-wide IP blacklists?
        'bypass_inactive_disable': None,     # boolean - Exempt this user from being disabled based on inactivity?
        'created_at': None,     # date-time - When this user was created
        'dav_permission': None,     # boolean - Can the user connect with WebDAV?
        'disabled': None,     # boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
        'email': None,     # email - User email address
        'ftp_permission': None,     # boolean - Can the user access with FTP/FTPS?
        'group_ids': None,     # string - Comma-separated list of group IDs of which this user is a member
        'header_text': None,     # string - Text to display to the user in the header of the UI
        'language': None,     # string - Preferred language
        'last_login_at': None,     # date-time - User's last login time
        'last_protocol_cipher': None,     # string - The last protocol and cipher used
        'lockout_expires': None,     # date-time - Time in the future that the user will no longer be locked out if applicable
        'name': None,     # string - User's full name
        'notes': None,     # string - Any internal notes on the user
        'notification_daily_send_time': None,     # int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
        'office_integration_enabled': None,     # boolean - Enable integration with Office for the web?
        'password_set_at': None,     # date-time - Last time the user's password was set
        'password_validity_days': None,     # int64 - Number of days to allow user to use the same password
        'public_keys_count': None,     # int64 - Number of public keys associated with this user
        'receive_admin_alerts': None,     # boolean - Should the user receive admin alerts such a certificate expiration notifications and overages?
        'require_2fa': None,     # boolean - Is 2fa required to sign in?
        'require_password_change': None,     # boolean - Is a password change required upon next user login?
        'restapi_permission': None,     # boolean - Can this user access the REST API?
        'self_managed': None,     # boolean - Does this user manage it's own credentials or is it a shared/bot user?
        'sftp_permission': None,     # boolean - Can the user access with SFTP?
        'site_admin': None,     # boolean - Is the user an administrator for this site?
        'skip_welcome_screen': None,     # boolean - Skip Welcome page in the UI?
        'ssl_required': None,     # string - SSL required setting
        'sso_strategy_id': None,     # int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
        'subscribe_to_newsletter': None,     # boolean - Is the user subscribed to the newsletter?
        'externally_managed': None,     # boolean - Is this user managed by a SsoStrategy?
        'time_zone': None,     # string - User time zone
        'type_of_2fa': None,     # string - Type(s) of 2FA methods in use.  Will be either `sms`, `totp`, `u2f`, `yubi`, or multiple values sorted alphabetically and joined by an underscore.
        'user_root': None,     # string - Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
        'avatar_file': None,     # file - An image file for your user avatar.
        'avatar_delete': None,     # boolean - If true, the avatar will be deleted.
        'change_password': None,     # string - Used for changing a password on an existing user.
        'change_password_confirmation': None,     # string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
        'grant_permission': None,     # string - Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
        'group_id': None,     # int64 - Group ID to associate this user with.
        'password': None,     # string - User password.
        'password_confirmation': None,     # string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
        'announcements_read': None,     # boolean - Signifies that the user has read all the announcements in the UI.
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in User.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in User.default_attributes if getattr(self, k, None) is not None}

    # Unlock user who has been locked out due to failed logins
    def unlock(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request("POST", "/users/{id}/unlock".format(id=params['id']), params, self.options)
        return response.data

    # Resend user welcome email
    def resend_welcome_email(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request("POST", "/users/{id}/resend_welcome_email".format(id=params['id']), params, self.options)
        return response.data

    # Trigger 2FA Reset process for user who has lost access to their existing 2FA methods
    def user_2fa_reset(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request("POST", "/users/{id}/2fa/reset".format(id=params['id']), params, self.options)
        return response.data

    # Parameters:
    #   avatar_file - file - An image file for your user avatar.
    #   avatar_delete - boolean - If true, the avatar will be deleted.
    #   change_password - string - Used for changing a password on an existing user.
    #   change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
    #   email - string - User's email.
    #   grant_permission - string - Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
    #   group_id - int64 - Group ID to associate this user with.
    #   group_ids - string - A list of group ids to associate this user with.  Comma delimited.
    #   password - string - User password.
    #   password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
    #   announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
    #   allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
    #   attachments_permission - boolean - Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
    #   authenticate_until - string - Scheduled Date/Time at which user will be deactivated
    #   authentication_method - string - How is this user authenticated?
    #   billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
    #   bypass_inactive_disable - boolean - Exempt this user from being disabled based on inactivity?
    #   bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
    #   dav_permission - boolean - Can the user connect with WebDAV?
    #   disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
    #   ftp_permission - boolean - Can the user access with FTP/FTPS?
    #   header_text - string - Text to display to the user in the header of the UI
    #   language - string - Preferred language
    #   notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
    #   name - string - User's full name
    #   notes - string - Any internal notes on the user
    #   office_integration_enabled - boolean - Enable integration with Office for the web?
    #   password_validity_days - int64 - Number of days to allow user to use the same password
    #   receive_admin_alerts - boolean - Should the user receive admin alerts such a certificate expiration notifications and overages?
    #   require_password_change - boolean - Is a password change required upon next user login?
    #   restapi_permission - boolean - Can this user access the REST API?
    #   self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
    #   sftp_permission - boolean - Can the user access with SFTP?
    #   site_admin - boolean - Is the user an administrator for this site?
    #   skip_welcome_screen - boolean - Skip Welcome page in the UI?
    #   ssl_required - string - SSL required setting
    #   sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
    #   subscribe_to_newsletter - boolean - Is the user subscribed to the newsletter?
    #   time_zone - string - User time zone
    #   user_root - string - Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
    #   username - string - User's username
    def update(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "change_password" in params and not isinstance(params["change_password"], str):
            raise InvalidParameterError("Bad parameter: change_password must be an str")
        if "change_password_confirmation" in params and not isinstance(params["change_password_confirmation"], str):
            raise InvalidParameterError("Bad parameter: change_password_confirmation must be an str")
        if "email" in params and not isinstance(params["email"], str):
            raise InvalidParameterError("Bad parameter: email must be an str")
        if "grant_permission" in params and not isinstance(params["grant_permission"], str):
            raise InvalidParameterError("Bad parameter: grant_permission must be an str")
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError("Bad parameter: group_ids must be an str")
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError("Bad parameter: password must be an str")
        if "password_confirmation" in params and not isinstance(params["password_confirmation"], str):
            raise InvalidParameterError("Bad parameter: password_confirmation must be an str")
        if "allowed_ips" in params and not isinstance(params["allowed_ips"], str):
            raise InvalidParameterError("Bad parameter: allowed_ips must be an str")
        if "authenticate_until" in params and not isinstance(params["authenticate_until"], str):
            raise InvalidParameterError("Bad parameter: authenticate_until must be an str")
        if "authentication_method" in params and not isinstance(params["authentication_method"], str):
            raise InvalidParameterError("Bad parameter: authentication_method must be an str")
        if "header_text" in params and not isinstance(params["header_text"], str):
            raise InvalidParameterError("Bad parameter: header_text must be an str")
        if "language" in params and not isinstance(params["language"], str):
            raise InvalidParameterError("Bad parameter: language must be an str")
        if "notification_daily_send_time" in params and not isinstance(params["notification_daily_send_time"], int):
            raise InvalidParameterError("Bad parameter: notification_daily_send_time must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "password_validity_days" in params and not isinstance(params["password_validity_days"], int):
            raise InvalidParameterError("Bad parameter: password_validity_days must be an int")
        if "ssl_required" in params and not isinstance(params["ssl_required"], str):
            raise InvalidParameterError("Bad parameter: ssl_required must be an str")
        if "sso_strategy_id" in params and not isinstance(params["sso_strategy_id"], int):
            raise InvalidParameterError("Bad parameter: sso_strategy_id must be an int")
        if "time_zone" in params and not isinstance(params["time_zone"], str):
            raise InvalidParameterError("Bad parameter: time_zone must be an str")
        if "user_root" in params and not isinstance(params["user_root"], str):
            raise InvalidParameterError("Bad parameter: user_root must be an str")
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError("Bad parameter: username must be an str")
        response, _options = Api.send_request("PATCH", "/users/{id}".format(id=params['id']), params, self.options)
        return response.data

    def delete(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request("DELETE", "/users/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `active`, `master_admin`, `site_id`, `authenticate_until`, `email`, `last_desktop_login_at`, `last_login_at`, `username`, `notes`, `site_admin`, `receive_admin_alerts`, `allowed_ips`, `password_validity_days`, `ssl_required` or `not_site_admin`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `username`, `email`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `username`, `email`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `username`, `email`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `username`, `email`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `username`, `email`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `username`, `email`, `notes`, `site_admin`, `allowed_ips`, `password_validity_days`, `ssl_required`, `last_login_at`, `authenticate_until` or `not_site_admin`.
#   ids - string - comma-separated list of User IDs
#   q[username] - string - List users matching username.
#   q[email] - string - List users matching email.
#   q[notes] - string - List users matching notes field.
#   q[admin] - string - If `true`, list only admin users.
#   q[allowed_ips] - string - If set, list only users with overridden allowed IP setting.
#   q[password_validity_days] - string - If set, list only users with overridden password validity days setting.
#   q[ssl_required] - string - If set, list only users with overridden SSL required setting.
#   search - string - Searches for partial matches of name, username, or email.
def list(params = {}, options = {}):
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
        raise InvalidParameterError("Bad parameter: filter_gt must be an dict")
    if "filter_gteq" in params and not isinstance(params["filter_gteq"], dict):
        raise InvalidParameterError("Bad parameter: filter_gteq must be an dict")
    if "filter_like" in params and not isinstance(params["filter_like"], dict):
        raise InvalidParameterError("Bad parameter: filter_like must be an dict")
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError("Bad parameter: filter_lteq must be an dict")
    if "ids" in params and not isinstance(params["ids"], str):
        raise InvalidParameterError("Bad parameter: ids must be an str")
    if "search" in params and not isinstance(params["search"], str):
        raise InvalidParameterError("Bad parameter: search must be an str")
    return ListObj(User,"GET", "/users", params, options)

def all(params = {}, options = {}):
    list(params, options)

# Parameters:
#   id (required) - int64 - User ID.
def find(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/users/{id}".format(id=params['id']), params, options)
    return User(response.data, options)

def get(id, params = {}, options = {}):
    find(id, params, options)

# Parameters:
#   avatar_file - file - An image file for your user avatar.
#   avatar_delete - boolean - If true, the avatar will be deleted.
#   change_password - string - Used for changing a password on an existing user.
#   change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
#   email - string - User's email.
#   grant_permission - string - Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
#   group_id - int64 - Group ID to associate this user with.
#   group_ids - string - A list of group ids to associate this user with.  Comma delimited.
#   password - string - User password.
#   password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
#   announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
#   allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
#   attachments_permission - boolean - Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
#   authenticate_until - string - Scheduled Date/Time at which user will be deactivated
#   authentication_method - string - How is this user authenticated?
#   billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
#   bypass_inactive_disable - boolean - Exempt this user from being disabled based on inactivity?
#   bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
#   dav_permission - boolean - Can the user connect with WebDAV?
#   disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
#   ftp_permission - boolean - Can the user access with FTP/FTPS?
#   header_text - string - Text to display to the user in the header of the UI
#   language - string - Preferred language
#   notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
#   name - string - User's full name
#   notes - string - Any internal notes on the user
#   office_integration_enabled - boolean - Enable integration with Office for the web?
#   password_validity_days - int64 - Number of days to allow user to use the same password
#   receive_admin_alerts - boolean - Should the user receive admin alerts such a certificate expiration notifications and overages?
#   require_password_change - boolean - Is a password change required upon next user login?
#   restapi_permission - boolean - Can this user access the REST API?
#   self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
#   sftp_permission - boolean - Can the user access with SFTP?
#   site_admin - boolean - Is the user an administrator for this site?
#   skip_welcome_screen - boolean - Skip Welcome page in the UI?
#   ssl_required - string - SSL required setting
#   sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
#   subscribe_to_newsletter - boolean - Is the user subscribed to the newsletter?
#   time_zone - string - User time zone
#   user_root - string - Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
#   username - string - User's username
def create(params = {}, options = {}):
    if "change_password" in params and not isinstance(params["change_password"], str):
        raise InvalidParameterError("Bad parameter: change_password must be an str")
    if "change_password_confirmation" in params and not isinstance(params["change_password_confirmation"], str):
        raise InvalidParameterError("Bad parameter: change_password_confirmation must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "grant_permission" in params and not isinstance(params["grant_permission"], str):
        raise InvalidParameterError("Bad parameter: grant_permission must be an str")
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    if "group_ids" in params and not isinstance(params["group_ids"], str):
        raise InvalidParameterError("Bad parameter: group_ids must be an str")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "password_confirmation" in params and not isinstance(params["password_confirmation"], str):
        raise InvalidParameterError("Bad parameter: password_confirmation must be an str")
    if "allowed_ips" in params and not isinstance(params["allowed_ips"], str):
        raise InvalidParameterError("Bad parameter: allowed_ips must be an str")
    if "authenticate_until" in params and not isinstance(params["authenticate_until"], str):
        raise InvalidParameterError("Bad parameter: authenticate_until must be an str")
    if "authentication_method" in params and not isinstance(params["authentication_method"], str):
        raise InvalidParameterError("Bad parameter: authentication_method must be an str")
    if "header_text" in params and not isinstance(params["header_text"], str):
        raise InvalidParameterError("Bad parameter: header_text must be an str")
    if "language" in params and not isinstance(params["language"], str):
        raise InvalidParameterError("Bad parameter: language must be an str")
    if "notification_daily_send_time" in params and not isinstance(params["notification_daily_send_time"], int):
        raise InvalidParameterError("Bad parameter: notification_daily_send_time must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "notes" in params and not isinstance(params["notes"], str):
        raise InvalidParameterError("Bad parameter: notes must be an str")
    if "password_validity_days" in params and not isinstance(params["password_validity_days"], int):
        raise InvalidParameterError("Bad parameter: password_validity_days must be an int")
    if "ssl_required" in params and not isinstance(params["ssl_required"], str):
        raise InvalidParameterError("Bad parameter: ssl_required must be an str")
    if "sso_strategy_id" in params and not isinstance(params["sso_strategy_id"], int):
        raise InvalidParameterError("Bad parameter: sso_strategy_id must be an int")
    if "time_zone" in params and not isinstance(params["time_zone"], str):
        raise InvalidParameterError("Bad parameter: time_zone must be an str")
    if "user_root" in params and not isinstance(params["user_root"], str):
        raise InvalidParameterError("Bad parameter: user_root must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    response, options = Api.send_request("POST", "/users", params, options)
    return User(response.data, options)

# Unlock user who has been locked out due to failed logins
def unlock(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("POST", "/users/{id}/unlock".format(id=params['id']), params, options)
    return response.data

# Resend user welcome email
def resend_welcome_email(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("POST", "/users/{id}/resend_welcome_email".format(id=params['id']), params, options)
    return response.data

# Trigger 2FA Reset process for user who has lost access to their existing 2FA methods
def user_2fa_reset(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("POST", "/users/{id}/2fa/reset".format(id=params['id']), params, options)
    return response.data

# Parameters:
#   avatar_file - file - An image file for your user avatar.
#   avatar_delete - boolean - If true, the avatar will be deleted.
#   change_password - string - Used for changing a password on an existing user.
#   change_password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `change_password`.
#   email - string - User's email.
#   grant_permission - string - Permission to grant on the user root.  Can be blank or `full`, `read`, `write`, `list`, or `history`.
#   group_id - int64 - Group ID to associate this user with.
#   group_ids - string - A list of group ids to associate this user with.  Comma delimited.
#   password - string - User password.
#   password_confirmation - string - Optional, but if provided, we will ensure that it matches the value sent in `password`.
#   announcements_read - boolean - Signifies that the user has read all the announcements in the UI.
#   allowed_ips - string - A list of allowed IPs if applicable.  Newline delimited
#   attachments_permission - boolean - Can the user create Bundles (aka Share Links)?  This field will be aliased or renamed in the future to `bundles_permission`.
#   authenticate_until - string - Scheduled Date/Time at which user will be deactivated
#   authentication_method - string - How is this user authenticated?
#   billing_permission - boolean - Allow this user to perform operations on the account, payments, and invoices?
#   bypass_inactive_disable - boolean - Exempt this user from being disabled based on inactivity?
#   bypass_site_allowed_ips - boolean - Allow this user to skip site-wide IP blacklists?
#   dav_permission - boolean - Can the user connect with WebDAV?
#   disabled - boolean - Is user disabled? Disabled users cannot log in, and do not count for billing purposes.  Users can be automatically disabled after an inactivity period via a Site setting.
#   ftp_permission - boolean - Can the user access with FTP/FTPS?
#   header_text - string - Text to display to the user in the header of the UI
#   language - string - Preferred language
#   notification_daily_send_time - int64 - Hour of the day at which daily notifications should be sent. Can be in range 0 to 23
#   name - string - User's full name
#   notes - string - Any internal notes on the user
#   office_integration_enabled - boolean - Enable integration with Office for the web?
#   password_validity_days - int64 - Number of days to allow user to use the same password
#   receive_admin_alerts - boolean - Should the user receive admin alerts such a certificate expiration notifications and overages?
#   require_password_change - boolean - Is a password change required upon next user login?
#   restapi_permission - boolean - Can this user access the REST API?
#   self_managed - boolean - Does this user manage it's own credentials or is it a shared/bot user?
#   sftp_permission - boolean - Can the user access with SFTP?
#   site_admin - boolean - Is the user an administrator for this site?
#   skip_welcome_screen - boolean - Skip Welcome page in the UI?
#   ssl_required - string - SSL required setting
#   sso_strategy_id - int64 - SSO (Single Sign On) strategy ID for the user, if applicable.
#   subscribe_to_newsletter - boolean - Is the user subscribed to the newsletter?
#   time_zone - string - User time zone
#   user_root - string - Root folder for FTP (and optionally SFTP if the appropriate site-wide setting is set.)  Note that this is not used for API, Desktop, or Web interface.
#   username - string - User's username
def update(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "change_password" in params and not isinstance(params["change_password"], str):
        raise InvalidParameterError("Bad parameter: change_password must be an str")
    if "change_password_confirmation" in params and not isinstance(params["change_password_confirmation"], str):
        raise InvalidParameterError("Bad parameter: change_password_confirmation must be an str")
    if "email" in params and not isinstance(params["email"], str):
        raise InvalidParameterError("Bad parameter: email must be an str")
    if "grant_permission" in params and not isinstance(params["grant_permission"], str):
        raise InvalidParameterError("Bad parameter: grant_permission must be an str")
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    if "group_ids" in params and not isinstance(params["group_ids"], str):
        raise InvalidParameterError("Bad parameter: group_ids must be an str")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "password_confirmation" in params and not isinstance(params["password_confirmation"], str):
        raise InvalidParameterError("Bad parameter: password_confirmation must be an str")
    if "allowed_ips" in params and not isinstance(params["allowed_ips"], str):
        raise InvalidParameterError("Bad parameter: allowed_ips must be an str")
    if "authenticate_until" in params and not isinstance(params["authenticate_until"], str):
        raise InvalidParameterError("Bad parameter: authenticate_until must be an str")
    if "authentication_method" in params and not isinstance(params["authentication_method"], str):
        raise InvalidParameterError("Bad parameter: authentication_method must be an str")
    if "header_text" in params and not isinstance(params["header_text"], str):
        raise InvalidParameterError("Bad parameter: header_text must be an str")
    if "language" in params and not isinstance(params["language"], str):
        raise InvalidParameterError("Bad parameter: language must be an str")
    if "notification_daily_send_time" in params and not isinstance(params["notification_daily_send_time"], int):
        raise InvalidParameterError("Bad parameter: notification_daily_send_time must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "notes" in params and not isinstance(params["notes"], str):
        raise InvalidParameterError("Bad parameter: notes must be an str")
    if "password_validity_days" in params and not isinstance(params["password_validity_days"], int):
        raise InvalidParameterError("Bad parameter: password_validity_days must be an int")
    if "ssl_required" in params and not isinstance(params["ssl_required"], str):
        raise InvalidParameterError("Bad parameter: ssl_required must be an str")
    if "sso_strategy_id" in params and not isinstance(params["sso_strategy_id"], int):
        raise InvalidParameterError("Bad parameter: sso_strategy_id must be an int")
    if "time_zone" in params and not isinstance(params["time_zone"], str):
        raise InvalidParameterError("Bad parameter: time_zone must be an str")
    if "user_root" in params and not isinstance(params["user_root"], str):
        raise InvalidParameterError("Bad parameter: user_root must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("PATCH", "/users/{id}".format(id=params['id']), params, options)
    return User(response.data, options)

def delete(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/users/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = {}, options = {}):
    delete(id, params, options)

def new(*args, **kwargs):
    return User(*args, **kwargs)