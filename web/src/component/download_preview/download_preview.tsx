
import ReactPlayer from 'react-player';
import { Image } from 'antd';
import './download_preview.css'

const DownloadPreview = ()=>{
    return (
        <div  className="grid-container">
            <div  className="grid-item">
                <Image src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"/>
            </div>
            <div className="grid-item">
                <div className="media-container">
                    <ReactPlayer
                        url="https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4"
                        controls
                        width="100%"
                        height="100%"
                        className="media-content"
                    />
                </div>
            </div>
        </div>
    )
}


export default DownloadPreview