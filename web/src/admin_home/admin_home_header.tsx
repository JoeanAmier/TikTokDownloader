import {Button, Col, Dropdown, Menu, Row, Space} from "antd";
import {Header} from "antd/es/layout/layout";



const items = [
    {key:'1', label:"占位符"},
    {key:'2', label:"占位符"},
    {key:'3', label:"占位符"},
]
const items2 = [
    {key:'1', label:"占位符"},
    {key:'2', label:"占位符"},
    {key:'3', label:"占位符"},
]

const AdminHomeHeader = ()=>{
    return (
        <Header className="home-header" style={{display: 'flex', alignItems: 'center', width: '100%'}}>
            <div className="demo-logo"/>
            <Menu
                mode="horizontal"
                items={items}
                style={{backgroundColor:"rgba(0, 0, 0, 0)", width:'85%', marginLeft:200}}
            />

            <Dropdown menu={{items,}} placement="bottomLeft">
                <Button style={{width:"5%",height:40}}>站位</Button>
            </Dropdown>

        </Header>
    )
}
export default AdminHomeHeader