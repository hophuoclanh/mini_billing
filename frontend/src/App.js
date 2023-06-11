import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Manager from './pages/manager'
import Login from './component/login'
import Product from './component/product'

function App(){
    return(
        <div>
            <BrowserRouter>
                <Routes>
                    <Route path='/' exact element={<Login />} />
                    <Route path='/manager'  element={<Manager />} />
                    <Route path='/product'  element={<Product />} />
                </Routes>
            </BrowserRouter>
        </div>
    )
}

export default App
