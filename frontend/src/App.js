import {BrwoserRounter, Routers, Router} from 'react-router-dom'

import Manager from './pages/manager'
import Login from './component/login'

function App(){
    return(
        <div>
            <BrwoserRounter>
                <Routers>
                    <Router path='/' exact element={<Login />} />
                    <Router path='/manager'  element={<Manager />} />
                </Routers>
            </BrwoserRounter>
        </div>
    )
}
