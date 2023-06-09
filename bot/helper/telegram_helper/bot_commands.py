from bot import CMD_SUFFIX


class _BotCommands:
    def __init__(self):
        self.StartCommand = 'start'
        self.MirrorCommand = [f'pea{CMD_SUFFIX}', f'm{CMD_SUFFIX}']
        self.UnzipMirrorCommand = [f'peaunzip{CMD_SUFFIX}', f'uzm{CMD_SUFFIX}']
        self.ZipMirrorCommand = [f'peazip{CMD_SUFFIX}', f'zm{CMD_SUFFIX}']
        self.QbMirrorCommand = [f'peaqb{CMD_SUFFIX}', f'qbm{CMD_SUFFIX}']
        self.QbUnzipMirrorCommand = [f'peaqbunzip{CMD_SUFFIX}', f'qbuzm{CMD_SUFFIX}']
        self.QbZipMirrorCommand = [f'peaqbzip{CMD_SUFFIX}', f'qbzm{CMD_SUFFIX}']
        self.YtdlCommand = [f'peaytdl{CMD_SUFFIX}', f'yt{CMD_SUFFIX}']
        self.YtdlZipCommand = [f'peaytdlzip{CMD_SUFFIX}', f'ytz{CMD_SUFFIX}']
        self.LeechCommand = [f'pealeech{CMD_SUFFIX}', f'l{CMD_SUFFIX}']
        self.UnzipLeechCommand = [f'peaunzipleech{CMD_SUFFIX}', f'uzl{CMD_SUFFIX}']
        self.ZipLeechCommand = [f'peazipleech{CMD_SUFFIX}', f'zl{CMD_SUFFIX}']
        self.QbLeechCommand = [f'peaqbleech{CMD_SUFFIX}', f'qbl{CMD_SUFFIX}']
        self.QbUnzipLeechCommand = [f'peaqbunzipleech{CMD_SUFFIX}', f'qbuzl{CMD_SUFFIX}']
        self.QbZipLeechCommand = [f'peaqbzipleech{CMD_SUFFIX}', f'qbzl{CMD_SUFFIX}']
        self.YtdlLeechCommand = [f'peaytdlleech{CMD_SUFFIX}', f'ytl{CMD_SUFFIX}']
        self.YtdlZipLeechCommand = [f'peaytdlzipleech{CMD_SUFFIX}', f'ytzl{CMD_SUFFIX}']
        self.CloneCommand = f'peaclone{CMD_SUFFIX}'
        self.CountCommand = f'peacount{CMD_SUFFIX}'
        self.DeleteCommand = f'peadel{CMD_SUFFIX}'
        self.CancelMirror = [f'peastop{CMD_SUFFIX}', f'cancel{CMD_SUFFIX}']
        self.CancelAllCommand = [f'peacancelall{CMD_SUFFIX}', 'cancelallbot']
        self.ListCommand = f'pealist{CMD_SUFFIX}'
        self.SearchCommand = f'peasearch{CMD_SUFFIX}'
        self.StatusCommand = [f'peastatus{CMD_SUFFIX}', 'sall']
        self.UsersCommand = f'peausers{CMD_SUFFIX}'
        self.AuthorizeCommand = f'peaauthorize{CMD_SUFFIX}'
        self.UnAuthorizeCommand = f'peaunauthorize{CMD_SUFFIX}'
        self.AddSudoCommand = f'peaaddsudo{CMD_SUFFIX}'
        self.RmSudoCommand = f'pearmsudo{CMD_SUFFIX}'
        self.PingCommand = [f'peaping{CMD_SUFFIX}','p']
        self.RestartCommand = [f'pearestart{CMD_SUFFIX}', 'restartall']
        self.StatsCommand = [f'peastats{CMD_SUFFIX}', 's']
        self.HelpCommand = f'peahelp{CMD_SUFFIX}'
        self.LogCommand = f'pealog{CMD_SUFFIX}'
        self.ShellCommand = f'peashell{CMD_SUFFIX}'
        self.EvalCommand = f'peaeval{CMD_SUFFIX}'
        self.ExecCommand = f'peaexec{CMD_SUFFIX}'
        self.ClearLocalsCommand = f'peaclearlocals{CMD_SUFFIX}'
        self.BotSetCommand = f'peabsetting{CMD_SUFFIX}'
        self.UserSetCommand = f'peausetting{CMD_SUFFIX}'
        self.BtSelectCommand = f'peabtsel{CMD_SUFFIX}'
        self.RssCommand = f'pearss{CMD_SUFFIX}'
        self.CategorySelect = f'peacatsel{CMD_SUFFIX}'
        self.RmdbCommand = f'pearmdb{CMD_SUFFIX}'

BotCommands = _BotCommands()
