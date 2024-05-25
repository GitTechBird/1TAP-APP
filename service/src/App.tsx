import { useState } from 'react'
import reactLogo from './assets/react.svg'
import { Route, RouterProvider, createBrowserRouter, createRoutesFromElements, Navigate, Outlet } from 'react-router-dom'
import './App.css'
import { FrappeProvider } from 'frappe-react-sdk'

export const ProtectedRoute = () => {
    return (
        <Outlet />
    )
}

export const ChannelRedirect = () => {
    const lastChannel = localStorage.getItem('ravenLastChannel') ?? 'general'
    return <Navigate to={`/channel/${lastChannel}`} replace />
}

export const ChannelRedirectNew = (props) => {
	console.log(props)
	if(props.path === 'login'){
		return (
			<h1>login-with-success</h1>
		)
	} else {
		return <Navigate to={`/login-with-email`} replace />
	}
}

const MainPage = () => {
	return(
		<>
			<h1>Main Page</h1>
			<Outlet />
		</>
		
	)
}

const router = createBrowserRouter(
	createRoutesFromElements(
	  <>
		<Route path='/login' element={<ChannelRedirectNew path="login"/>} />
		<Route path='/login-with-email' element={<h1>login-with-email</h1>} />
		<Route path="/" element={<ProtectedRoute />}>
		  <Route index element={<ChannelRedirect />} />
		  <Route path="channel" element={<MainPage />} >
			<Route index element={<ChannelRedirect />} />
			<Route path="saved-messages" element={<h1>saved-messages</h1>} />
			<Route path=":channelID" element={<h1>channelID</h1>} />
		  </Route>
		</Route>
		<Route path="*" element={<ChannelRedirectNew />} replace/>
	  </>
	), {
	basename: `/service` ?? '',
  }
  )
  
function App() {
  const [count, setCount] = useState(0)

  return (
	<div className="App">
	  <FrappeProvider>
	  	<RouterProvider router={router} fallbackElement={<h1>fallbackElement</h1>} />
	  </FrappeProvider>
	</div>
  )
}

export default App
