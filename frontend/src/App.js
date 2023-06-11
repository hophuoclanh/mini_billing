import {BrowserRouter, Routes, Route} from 'react-router-dom'

import Createuser from './component/Create/create_user'
import Main from './route/main'

function App(){
    return(
        <div>
            <BrowserRouter>
                <Routes>
                    <Route path='/' exact element={<Main/>} />
                    <Route path='/createuser' exact element={<Createuser/>} />
                </Routes>
            </BrowserRouter>
        </div>
    )
}

export default App