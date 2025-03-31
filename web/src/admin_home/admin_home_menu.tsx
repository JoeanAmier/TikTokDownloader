import {Menu} from "antd";
import { useLocation} from "react-router-dom";
import {useState, useEffect} from 'react'
import {MenuItems} from './menu_items.tsx'




const AdminHomeMenu = ()=>{
    const location = useLocation()
    const [currentSelect, setCurrentSelect] = useState(location.pathname)
    useEffect(()=>{
        setCurrentSelect(location.pathname)
    },[location])

    const findKeyByPath = (path, items) => {
        for (const item of items) {
            if (item.path === path) {
                return item.key;
            }

            if (item.children) {
                const childKey = findKeyByPath(path, item.children);
                if (childKey) {
                    return childKey;
                }
            }
        }

        return null;
    };
    return (
        <Menu  selectedKeys={findKeyByPath(currentSelect, MenuItems)} mode="inline"
               style={{height: '98%', borderRight: 0, backgroundColor: "#e3ccc4",borderRadius: 15, marginTop:15}}
               items={MenuItems}/>
    )
}

export default AdminHomeMenu