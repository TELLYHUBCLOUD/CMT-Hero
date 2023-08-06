from bot import CMD_SUFFIX


class _BotCommands:
    def __init__(self):
        self.StartCommand = 'start'
        self.MirrorCommand = [f'msb{CMD_SUFFIX}', f'pmsb{CMD_SUFFIX}']
        self.QbMirrorCommand = [f'msbqb{CMD_SUFFIX}', f'pqmsb{CMD_SUFFIX}']
        self.YtdlCommand = [f'msbytdl{CMD_SUFFIX}', f'ytmsb{CMD_SUFFIX}']
        self.LeechCommand = [f'msbleech{CMD_SUFFIX}', f'lmsb{CMD_SUFFIX}']
        self.QbLeechCommand = [f'msbqbleech{CMD_SUFFIX}', f'qblmsb{CMD_SUFFIX}']
        self.YtdlLeechCommand = [f'msbytdlleech{CMD_SUFFIX}', f'ytlmsb{CMD_SUFFIX}']
        self.CloneCommand = f'msbclone{CMD_SUFFIX}'
        self.CountCommand = f'msbcount{CMD_SUFFIX}'
        self.DeleteCommand = f'peadel{CMD_SUFFIX}'
        self.CancelMirror = f'c{CMD_SUFFIX}'
        self.CancelAllCommand = [f'msbcancelall{CMD_SUFFIX}', 'cancelallbot']
        self.ListCommand = f'msblist{CMD_SUFFIX}'
        self.SearchCommand = f'msbsearch{CMD_SUFFIX}'
        self.StatusCommand = [f'msbstatus{CMD_SUFFIX}', 'sallmsb']
        self.UsersCommand = f'msbusers{CMD_SUFFIX}'
        self.AuthorizeCommand = f'msbauthorize{CMD_SUFFIX}'
        self.UnAuthorizeCommand = f'msbunauthorize{CMD_SUFFIX}'
        self.AddSudoCommand = f'msbaddsudo{CMD_SUFFIX}'
        self.RmSudoCommand = f'msbrmsudo{CMD_SUFFIX}'
        self.PingCommand = [f'msbping{CMD_SUFFIX}','ping']
        self.RestartCommand = [f'msbrestart{CMD_SUFFIX}', 'restartall']
        self.StatsCommand = [f'msbstats{CMD_SUFFIX}', 'smsb']
        self.HelpCommand = f'msbhelp{CMD_SUFFIX}'
        self.LogCommand = f'msblog{CMD_SUFFIX}'
        self.ShellCommand = f'msbshell{CMD_SUFFIX}'
        self.EvalCommand = f'msbeval{CMD_SUFFIX}'
        self.ExecCommand = f'msbexec{CMD_SUFFIX}'
        self.ClearLocalsCommand = f'msbclearlocals{CMD_SUFFIX}'
        self.BotSetCommand = f'msbbsetting{CMD_SUFFIX}'
        self.UserSetCommand = f'msbusetting{CMD_SUFFIX}'
        self.BtSelectCommand = f'msbbtsel{CMD_SUFFIX}'
        self.RssCommand = f'msbrss{CMD_SUFFIX}'
        self.CategorySelect = f'msbcatsel{CMD_SUFFIX}'
        self.RmdbCommand = f'msbrmdb{CMD_SUFFIX}'

BotCommands = _BotCommands()
