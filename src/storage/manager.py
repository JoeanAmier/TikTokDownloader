from typing import TYPE_CHECKING

from .csv import CSVLogger
from .sqlite import SQLLogger
from .text import BaseTextLogger
from .xlsx import XLSXLogger

if TYPE_CHECKING:
    from ..config import Parameter

__all__ = ["RecordManager"]


class RecordManager:
    """检查数据储存路径和文件夹"""
    detail = (
        ("type", "作品类型", "TEXT",),
        ("collection_time", "采集时间", "TEXT",),
        ("uid", "UID", "TEXT",),
        ("sec_uid", "SEC_UID", "TEXT",),
        ("unique_id", "ID", "TEXT",),
        # ("short_id", "SHORT_ID", "TEXT",),
        ("id", "作品ID", "TEXT",),
        ("desc", "作品描述", "TEXT",),
        ("text_extra", "作品话题", "TEXT",),
        ("duration", "视频时长", "TEXT",),
        ("ratio", "视频分辨率", "TEXT",),
        ("height", "视频高度", "INTEGER",),
        ("width", "视频宽度", "INTEGER",),
        ("share_url", "作品链接", "TEXT",),
        ("create_time", "发布时间", "TEXT",),
        ("uri", "视频URI", "TEXT",),
        ("nickname", "账号昵称", "TEXT",),
        ("user_age", "年龄", "INTEGER",),
        ("signature", "账号签名", "TEXT",),
        ("downloads", "下载地址", "TEXT",),
        ("music_author", "音乐作者", "TEXT",),
        ("music_title", "音乐标题", "TEXT",),
        ("music_url", "音乐链接", "TEXT",),
        ("origin_cover", "静态封面", "TEXT",),
        ("dynamic_cover", "动态封面", "TEXT",),
        ("tag", "隐藏标签", "TEXT",),
        ("digg_count", "点赞数量", "INTEGER",),
        ("comment_count", "评论数量", "INTEGER",),
        ("collect_count", "收藏数量", "INTEGER",),
        ("share_count", "分享数量", "INTEGER",),
        ("play_count", "播放数量", "INTEGER",),
        ("extra", "额外信息", "TEXT",),
    )
    comment = (
        ("collection_time", "采集时间", "TEXT",),
        ("cid", "评论ID", "TEXT",),
        ("create_time", "评论时间", "TEXT",),
        ("uid", "UID", "TEXT",),
        ("sec_uid", "SEC_UID", "TEXT",),
        # ("short_id", "SHORT_ID", "TEXT",),
        # ("unique_id", "抖音号", "TEXT",),
        ("nickname", "账号昵称", "TEXT",),
        ("signature", "账号签名", "TEXT",),
        ("user_age", "年龄", "INTEGER",),
        ("ip_label", "IP归属地", "TEXT",),
        ("text", "评论内容", "TEXT",),
        ("sticker", "评论表情", "TEXT",),
        ("image", "评论图片", "TEXT",),
        ("digg_count", "点赞数量", "INTEGER",),
        ("reply_comment_total", "回复数量", "INTEGER",),
        ("reply_id", "回复ID", "TEXT",),
        ("reply_to_reply_id", "回复对象", "TEXT",),
    )
    user = (
        ("collection_time", "采集时间", "TEXT",),
        ("nickname", "昵称昵称", "TEXT",),
        ("url", "账号链接", "TEXT",),
        ("signature", "账号签名", "TEXT",),
        ("unique_id", "抖音号", "TEXT",),
        ("user_age", "年龄", "INTEGER",),
        ("gender", "性别", "TEXT",),
        ("country", "国家", "TEXT",),
        ("province", "省份", "TEXT",),
        ("city", "城市", "TEXT",),
        ("district", "地区", "TEXT",),
        ("ip_location", "IP归属地", "TEXT",),
        ("verify", "标签", "TEXT",),
        ("enterprise", "企业", "TEXT",),
        ("sec_uid", "SEC_UID", "TEXT",),
        ("uid", "UID", "TEXT",),
        ("short_id", "SHORT_ID", "TEXT",),
        ("avatar", "头像链接", "TEXT",),
        ("cover", "背景图链接", "TEXT",),
        ("aweme_count", "作品数量", "INTEGER",),
        ("total_favorited", "获赞数量", "INTEGER",),
        ("favoriting_count", "喜欢数量", "INTEGER",),
        ("follower_count", "粉丝数量", "INTEGER",),
        ("following_count", "关注数量", "INTEGER",),
        ("max_follower_count", "粉丝最大值", "INTEGER",),
    )
    user_tiktok = (
        ("collection_time", "采集时间", "TEXT",),
        ("nickname", "昵称昵称", "TEXT",),
        ("url", "账号链接", "TEXT",),
        ("signature", "账号签名", "TEXT",),
        ("uniqueId", "抖音号", "TEXT",),
        ("avatarThumb", "缩略头像链接", "TEXT",),
        ("avatarMedium", "中图头像链接", "TEXT",),
        ("avatarLarger", "大图头像链接", "TEXT",),
        ("secUid", "SEC_UID", "TEXT",),
        ("link", "用户设置链接", "TEXT",),
        ("risk", "链接风险", "INTEGER",),
        ("videoCount", "作品数量", "INTEGER",),
        ("heartCount", "获赞数量", "INTEGER",),
        ("followerCount", "粉丝数量", "INTEGER",),
        ("followingCount", "关注数量", "INTEGER",),
        ("stitchSetting", "拼接设置", "INTEGER",),
        ("privateAccount", "是否允许嵌入", "INTEGER",),
        ("isEmbedBanned", "账号是否被禁止使用嵌入功能", "BOOL",),
        ("isADVirtual", "是否为广告虚拟号", "BOOL",),
        ("openFavorite", "是否开放喜欢列表", "BOOL",),
        ("privateAccount", "是否为私有账户", "BOOL",),
        ("canExpPlaylist", "是否允许导出播放列表", "BOOL",),
        ("verified", "标签", "BOOL",),
        ("ttSeller", "认证商家", "BOOL",),
    )
    search_user = (
        ("collection_time", "采集时间", "TEXT",),
        ("uid", "UID", "TEXT",),
        ("sec_uid", "SEC_UID", "TEXT",),
        ("nickname", "账号昵称", "TEXT",),
        ("unique_id", "抖音号", "TEXT",),
        ("short_id", "SHORT_ID", "TEXT",),
        ("avatar", "头像链接", "TEXT",),
        ("signature", "账号签名", "TEXT",),
        ("verify", "标签", "TEXT",),
        ("enterprise", "企业", "TEXT",),
        ("follower_count", "粉丝数量", "INTEGER",),
        ("total_favorited", "获赞数量", "INTEGER",),
    )
    search_live = (
        ("collection_time", "采集时间", "TEXT",),
        ("room_id", "直播ID", "TEXT",),
        ("uid", "UID", "TEXT",),
        ("sec_uid", "SEC_UID", "TEXT",),
        ("nickname", "账号昵称", "TEXT",),
        ("short_id", "SHORT_ID", "TEXT",),
        ("avatar", "头像链接", "TEXT",),
        ("signature", "账号签名", "TEXT",),
        ("verify", "标签", "TEXT",),
        ("enterprise", "企业", "TEXT",),
    )
    hot = (
        ("position", "排名", "INTEGER",),
        ("word", "内容", "TEXT",),
        ("hot_value", "热度", "INTEGER",),
        ("cover", "封面", "TEXT",),
        ("event_time", "时间", "TEXT",),
        ("view_count", "浏览数量", "INTEGER",),
        ("video_count", "视频数量", "INTEGER",),
        ("sentence_id", "SENTENCE_ID", "TEXT",),
    )

    detail_keys = [i[0] for i in detail]
    detail_name = [i[1] for i in detail]
    detail_type = [i[2] for i in detail]
    comment_keys = [i[0] for i in comment]
    comment_name = [i[1] for i in comment]
    comment_type = [i[2] for i in comment]
    user_keys = [i[0] for i in user]
    user_name = [i[1] for i in user]
    user_type = [i[2] for i in user]
    user_tiktok_keys = [i[0] for i in user_tiktok]
    user_tiktok_name = [i[1] for i in user_tiktok]
    user_tiktok_type = [i[2] for i in user_tiktok]
    search_user_keys = [i[0] for i in search_user]
    search_user_name = [i[1] for i in search_user]
    search_user_type = [i[2] for i in search_user]
    search_live_keys = [i[0] for i in search_live]
    search_live_name = [i[1] for i in search_live]
    search_live_type = [i[2] for i in search_live]
    hot_keys = [i[0] for i in hot]
    hot_name = [i[1] for i in hot]
    hot_type = [i[2] for i in hot]

    LoggerParams = {
        "detail": {
            "db_name": "DetailData.db",
            "title_line": detail_name,
            "title_type": detail_type,
            "field_keys": detail_keys,
        },
        "comment": {
            "db_name": "CommentData.db",
            "title_line": comment_name,
            "title_type": comment_type,
            "field_keys": comment_keys,
        },
        "user": {
            "db_name": "UserData.db",
            "title_line": user_name,
            "title_type": user_type,
            "field_keys": user_keys,
        },
        "user_tiktok":{
            "db_name": "UserTikTokData.db",
            "title_line": user_tiktok_name,
            "title_type": user_tiktok_type,
            "field_keys": user_tiktok_keys,
        },
        "mix": {
            "db_name": "MixData.db",
            "title_line": detail_name,
            "title_type": detail_type,
            "field_keys": detail_keys,
        },
        "search_general": {
            "db_name": "SearchData.db",
            "title_line": detail_name,
            "title_type": detail_type,
            "field_keys": detail_keys,
        },
        "search_user": {
            "db_name": "SearchData.db",
            "title_line": search_user_name,
            "title_type": search_user_type,
            "field_keys": search_user_keys,
        },
        "search_live": {
            "db_name": "SearchData.db",
            "title_line": search_live_name,
            "title_type": search_live_type,
            "field_keys": search_live_keys,
        },
        "hot": {
            "db_name": "BoardData.db",
            "title_line": hot_name,
            "title_type": hot_type,
            "field_keys": hot_keys,
        },
    }
    DataLogger = {
        "csv": CSVLogger,
        "xlsx": XLSXLogger,
        "sql": SQLLogger,
        # "mysql": BaseTextLogger,
    }

    def run(
            self,
            parameter: "Parameter",
            folder="",
            type_="detail",
            blank=False,
    ):
        root = parameter.root.joinpath(
            parameter.CLEANER.filter_name(folder, "Data"))
        root.mkdir(exist_ok=True)
        params = self.LoggerParams[type_]
        logger = BaseTextLogger if blank else self.DataLogger.get(
            parameter.storage_format, BaseTextLogger)
        return root, params, logger
