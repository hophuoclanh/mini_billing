import { useState } from 'react'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Box  from '@mui/material/Box'

import RadioGroup from '@mui/material/RadioGroup'
import FormControlLabel from '@mui/material/FormControlLabel'


import SendIcon from '@mui/icons-material/Send'
import { Radio } from '@mui/material'

function Createuser(){
    const [name, setName] = useState ('')
    const [phone, setPhone] = useState('')
    const [email, setEmail] = useState('')
    const [password,setPassword] = useState('')
    const [address, setAddress] = useState('')
    const [nameError,setNameError ]= useState(false)
    const [phoneError,setPhoneError ]= useState(false)
    const [emailError,setEmailError ]= useState(false)
    const [passwordError,setPasswordError ]= useState(false)
    const [addressError,setAddressError ]= useState(false)

    const [role,setRole]= useState('staff')

    const handleSubmit = (e) => {
        e.preventDefault()

        if (name && phone && email && password && address && role) {
            console.log(name, phone, email,  address, password, role)
        }

        if(name === ''){
            setNameError(true)
        }
        if(phone === ''){
            setPhoneError(true)
        }
        if(email === ''){
            setEmailError(true)
        }
        if(password === ''){
            setPasswordError(true)
        }
        if(address === ''){
            setAddressError(true)
        }
    }

    return (
        <Container >
            <Typography variant='h3' align='center' gutterBottom>
                Create User
            </Typography>
            <form noValidate autoComplete='off' onSubmit={handleSubmit}>
                <Box padding={2}>
                    <TextField 
                    label='Name' 
                    variant='standard' 
                    fullWidth 
                    required 
                    onChange={(e) => setName(e.target.value)} 
                    error={nameError}
                    />
                    <TextField 
                    label='Phone' 
                    variant='standard' 
                    fullWidth 
                    required 
                    onChange={(e) => setPhone(e.target.value)}
                    error={phoneError}
                    />
                    <TextField 
                    label='Email' 
                    variant='standard' 
                    fullWidth 
                    required 
                    onChange={(e) => setEmail(e.target.value)}
                    error={emailError}
                    />
                    <TextField 
                    label='Password' 
                    variant='standard' 
                    fullWidth 
                    required 
                    onChange={(e) => setPassword(e.target.value)}
                    error={passwordError}
                    />
                    <TextField 
                    label='Address' 
                    variant='standard' 
                    fullWidth 
                    required 
                    onChange={(e) => setAddress(e.target.value)}
                    error={addressError}
                    />
                    <RadioGroup 
                    row 
                    value={role} 
                    onChange={e => setRole(e.target.value)}
                    >
                        <FormControlLabel 
                        value='admin' 
                        control={<Radio />} 
                        label='Admin' />
                        <FormControlLabel 
                        value='manager' 
                        control={<Radio />} 
                        label='Manager' />
                        <FormControlLabel 
                        value='staff' 
                        control={<Radio />} 
                        label='Staff' />
                    </RadioGroup>
                </Box>
                <Button type='submit' variant='contained' startIcon={<SendIcon />}>Submit</Button>
            </form>
        </Container>
    )
}

export default Createuser