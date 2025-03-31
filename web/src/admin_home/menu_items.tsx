import {
    ClockCircleOutlined, CloudDownloadOutlined, DownloadOutlined, SettingOutlined,
    VideoCameraAddOutlined, ToolOutlined} from "@ant-design/icons";
import {Link} from "react-router-dom";


const MenuItems = [
    {
        key: '1',
        icon: <DownloadOutlined />,
        label: <Link to="/download_work">作品下载</Link> ,
        path:"/download_work",
        cn:"作品下载"
    },
    {
        key: '2',
        icon: <CloudDownloadOutlined />,
        label: <Link to="/download_batch">批量下载</Link> ,
        path:"/download_batch",
        cn:"批量下载"
    },
    {
        key: '3',
        icon: <SettingOutlined />,
        label: <Link to="/download_settings">下载配置</Link> ,
        path:"/download_settings",
        cn:"下载配置"
    },
    {
        key: '4',
        icon: <ClockCircleOutlined />,
        label: <Link to="/download_record">下载记录</Link> ,
        path:"/download_record",
        cn:"下载记录"
    },
    {
        key: '5',
        icon: <VideoCameraAddOutlined />,
        label: <Link to="/download_preview">下载预览</Link> ,
        path:"/download_preview",
        cn:"下载预览"
    },
    {
        key: '6',
        icon: <ToolOutlined />,
        label: <Link to="/other_function">其他功能</Link> ,
        path:"/other_function",
        cn:"其他功能"
    },
]

export {MenuItems}