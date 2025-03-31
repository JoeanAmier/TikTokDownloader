import { createBrowserRouter, RouteObject } from 'react-router-dom';
import AdminHome from './admin_home/admin_home.tsx'
import DownloadBatch from "./component/download_batch/download_batch.tsx";
import DownloadPreview from "./component/download_preview/download_preview.tsx";
import DownloadRecord from "./component/download_record/download_record.tsx";
import DownloadSettings from "./component/download_settings/download_settings.tsx";
import DownloadWork from "./component/download_work/download_work.tsx";
import OtherFunction from "./component/other_function/other_function.tsx";


const routes: RouteObject[] = [
  {
    path: "/",
    element: <AdminHome />,
    children: [
      {
        path:"/download_work",
        element:<DownloadWork/>
      },
      {
        path:"/download_batch",
        element:<DownloadBatch/>
      },
      {
        path:"/download_settings",
        element:<DownloadSettings/>
      },
      {
        path:"/download_record",
        element:<DownloadRecord/>
      },
      {
        path:"/download_preview",
        element:<DownloadPreview/>
      },
      {
        path:"/other_function",
        element:<OtherFunction/>
      }
    ]
  } as RouteObject ,
];

const httpRouter = createBrowserRouter(routes);
export default httpRouter;