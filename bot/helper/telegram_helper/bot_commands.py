from bot import CMD_SUFFIX


class _BotCommands:
    def __init__(self):
        self.StartCommand = 'start1'
        self.MirrorCommand = [f'pea1{CMD_SUFFIX}', f'p{CMD_SUFFIX}']
        self.QbMirrorCommand = [f'pea1qb{CMD_SUFFIX}', f'pq{CMD_SUFFIX}']
        self.YtdlCommand = [f'pea1ytdl{CMD_SUFFIX}', f'yt{CMD_SUFFIX}']
        self.LeechCommand = [f'pea1leech{CMD_SUFFIX}', f'l{CMD_SUFFIX}']
        self.QbLeechCommand = [f'pea1qbleech{CMD_SUFFIX}', f'qbl{CMD_SUFFIX}']
        self.YtdlLeechCommand = [f'pea1ytdlleech{CMD_SUFFIX}', f'ytl{CMD_SUFFIX}']
        self.CloneCommand = f'pea1clone{CMD_SUFFIX}'
        self.CountCommand = f'pea1count{CMD_SUFFIX}'
        self.DeleteCommand = f'peadel{CMD_SUFFIX}'
        self.CancelMirror = f'c{CMD_SUFFIX}'
        self.CancelAllCommand = [f'pea1cancelall{CMD_SUFFIX}', 'cancelallbot']
        self.ListCommand = f'pea1list{CMD_SUFFIX}'
        self.SearchCommand = f'pea1search{CMD_SUFFIX}'
        self.StatusCommand = [f'pea1status{CMD_SUFFIX}', 'sall']
        self.UsersCommand = f'pea1users{CMD_SUFFIX}'
        self.AuthorizeCommand = f'pea1authorize{CMD_SUFFIX}'
        self.UnAuthorizeCommand = f'pea1unauthorize{CMD_SUFFIX}'
        self.AddSudoCommand = f'pea1addsudo{CMD_SUFFIX}'
        self.RmSudoCommand = f'pea1rmsudo{CMD_SUFFIX}'
        self.PingCommand = [f'pea1ping{CMD_SUFFIX}','p']
        self.RestartCommand = [f'pea1restart{CMD_SUFFIX}', 'restartall']
        self.StatsCommand = [f'pea1stats{CMD_SUFFIX}', 's']
        self.HelpCommand = f'pea1help{CMD_SUFFIX}'
        self.LogCommand = f'pea1log{CMD_SUFFIX}'
        self.ShellCommand = f'pea1shell{CMD_SUFFIX}'
        self.EvalCommand = f'pea1eval{CMD_SUFFIX}'
        self.ExecCommand = f'pea1exec{CMD_SUFFIX}'
        self.ClearLocalsCommand = f'pea1clearlocals{CMD_SUFFIX}'
        self.BotSetCommand = f'pea1bsetting{CMD_SUFFIX}'
        self.UserSetCommand = f'pea1usetting{CMD_SUFFIX}'
        self.BtSelectCommand = f'pea1btsel{CMD_SUFFIX}'
        self.RssCommand = f'pea1rss{CMD_SUFFIX}'
        self.CategorySelect = f'pea1catsel{CMD_SUFFIX}'
        self.RmdbCommand = f'pea1rmdb{CMD_SUFFIX}'

BotCommands = _BotCommands()
