import time, os, yaml, re


def yaml_loader(yaml_file):
    loader = yaml.SafeLoader
    loader.add_implicit_resolver(
        u'tag:yaml.org,2002:float',
        re.compile(u'''^(?:
        [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
        |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
        |\\.[0-9_]+(?:[eE][-+][0-9]+)?
        |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
        |[-+]?\\.(?:inf|Inf|INF)
        |\\.(?:nan|NaN|NAN))$''', re.X),
        list(u'-+0123456789.')
    )
    with open(yaml_file) as f:
        config = yaml.load(f, Loader=loader) # cfg dict
    return config


class DriverInfomation(object):
    def __init__(self, config):
        self.ref_url = config["ref_url"]
        self.driver_path = config["driver_path"]
        self.LinkRetweet = config["twitter_link"]
        self.LinkTelegram = config["telegram_link"]


class UserInfomation(object):
    def __init__(self, config):
        self.TwitterUsername = config["twitter_username"]
        self.TelegramUsername = config["telegram_username"]
        self.WalletPassword = config["pass_wallet"]
        self.FirefoxProfile = None
    
    def create_quote(self, content = 'good', hashTag= '#', tag = 'DeFiLand'):
        result = content + "\n" + hashTag + "\n" + tag + " "
        return result

