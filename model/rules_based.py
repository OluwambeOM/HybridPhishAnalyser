def check_phishing_keywords(subject, body):
    phishing_keywords = [
        'urgent', 'win', 'prize', 'click here', 'verify', 'account',
        'security alert', 'password', 'confirm', 'limited time',
        'free', 'offer', 'bank', 'lottery', 'reset your password',
        'suspended account', 'unauthorized access'
    ]
    for keyword in phishing_keywords:
        if keyword in subject.lower() or keyword in body.lower():
            return 1  # Flag as phishing
    return 0  # Not phishing

def check_sender_domain(sender_email):
    suspicious_domains = ['@gmail.com', '@yahoo.com', '@hotmail.com', '@outlook.com']
    domain = sender_email.split('@')[-1]
    if domain in suspicious_domains:
        return 1  # Flag as phishing
    return 0  # Not phishing

def check_suspicious_urls(body):
    suspicious_urls = re.findall(r'http[s]?://[^\s]+', body)
    for url in suspicious_urls:
        if 'login' in url or 'verify' in url or 'update' in url:
            return 1  # Flag as phishing
    return 0  # Not phishing

def check_language_tone(body):
    suspicious_phrases = [
        'act now', 'immediate action required', 'final notice',
        'free gift', 'limited offer', 'your account has been compromised',
        'click to claim', 'verify your identity'
    ]
    for phrase in suspicious_phrases:
        if phrase in body.lower():
            return 1  # Flag as phishing
    return 0  # Not phishing

def check_attachments(attachment_list):
    suspicious_filetypes = ['.exe', '.scr', '.bat', '.docm', '.xlsm', '.zip', '.rar']
    for attachment in attachment_list:
        if any(attachment.lower().endswith(ext) for ext in suspicious_filetypes):
            return 1  # Flag as phishing
    return 0  # Not phishing

def rules_based_filter(subject, body, sender_email=None, attachment_list=None):
    phishing_score = 0
    phishing_score += check_phishing_keywords(subject, body) * 2
    if sender_email:
        phishing_score += check_sender_domain(sender_email) * 2
    phishing_score += check_suspicious_urls(body) * 3
    phishing_score += check_language_tone(body) * 1
    if attachment_list:
        phishing_score += check_attachments(attachment_list) * 2
    return 1 if phishing_score >= 5 else 0
