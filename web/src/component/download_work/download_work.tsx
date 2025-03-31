
import {Input, Button, Form} from 'antd';
const { TextArea } = Input;
import React from 'react';
import { Descriptions } from 'antd';
import type { DescriptionsProps } from 'antd';

const itemsDesc: DescriptionsProps['items'] = [
    {
        key: '3',
        label: '用户名称',
        children: '叼毛',
    },
    {
        key: '4',
        label: '作品id',
        children: 'aaaaa',
    },

    {
        key: '5',
        label: '用户id',
        children: '12345678',
    },
    {
        key: '6',
        label: '作品描述',
        children: 'No. 18, Wantang Road, Xihu District, Hangzhou, Zhejiang, China',
    },
];


const DownloadWork = ()=>{
    const [form] = Form.useForm();
    const onFormLayoutChange = ({  }) => {

    };

    return (
        <div style={{marginTop: "2%", marginLeft: "10%", marginRight: "10%", height: "100%",}}>
            <div>
                <Form form={form} onValuesChange={onFormLayoutChange}  >
                    <Form.Item ><TextArea placeholder="视频下载" style={{resize:"none", height:50}}/></Form.Item>
                    <Form.Item style={{display: 'flex', justifyContent: 'center'}}>
                        <Button type="primary" style={{width: 150}}>下载</Button>
                        <Button type="primary" style={{width: 150, marginLeft:10}}>提取</Button>
                        <Button type="primary" style={{width: 150, marginLeft:10}}>搜索</Button>
                    </Form.Item>

                </Form>
            </div>
            <div style={{display: 'flex', justifyContent: 'center', marginTop:50, height: "100%", }}>
                <div style={{width:"100%", backgroundColor:"#fff", borderRadius:25, padding:25, height:"20%"}}>
                    <Descriptions  items={itemsDesc} bordered={true} column={2}/>
                </div>

            </div>

        </div>
    )
}

export default DownloadWork