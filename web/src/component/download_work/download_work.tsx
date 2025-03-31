
import {Input, Button, Form} from 'antd';
const { TextArea } = Input;
const DownloadWork = ()=>{
    const [form] = Form.useForm();
    const onFormLayoutChange = ({ layout }) => {

    };

    return (
        <div style={{marginTop: "2%"}}>
            <Form form={form} onValuesChange={onFormLayoutChange} >
                <Form.Item wrapperCol={{ offset: 1, span: 18 }}>多个链接使用换行分隔</Form.Item>
                <Form.Item label="视频下载"><TextArea placeholder="" style={{resize:"none", height:150}}/></Form.Item>
                <Form.Item style={{display: 'flex', justifyContent: 'center'}}>
                    <Button type="primary" style={{width: 300}}>下载</Button>
                </Form.Item>

            </Form>

        </div>
    )
}

export default DownloadWork