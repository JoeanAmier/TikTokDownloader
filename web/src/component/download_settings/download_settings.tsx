
import  { useState } from 'react';
import { Button, Form, Input, Radio } from 'antd';

const DownloadSettings = ()=>{
    const [form] = Form.useForm();
    const onFormLayoutChange = ({ layout }) => {

    };
    return (
        <div style={{marginTop:"2%"}}>
            <Form form={form} onValuesChange={onFormLayoutChange} labelCol={{ span: 2 }} wrapperCol={{ span: 20 }}>
                <Form.Item label="cookie"><Input placeholder="" /></Form.Item>
                <Form.Item label="代理"><Input placeholder="" /></Form.Item>
                <Form.Item label="下载路径"><Input placeholder="" /></Form.Item>
                <Form.Item style={{ display: 'flex', justifyContent: 'center' }}>
                    <Button type="primary" style={{ width: 300 }}>提交修改</Button>
                </Form.Item>
            </Form>

        </div>
    )
}

export default DownloadSettings