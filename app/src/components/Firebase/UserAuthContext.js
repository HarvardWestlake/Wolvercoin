import React, { createContext, useContext, useEffect, useState } from "react"

//import auth from "firebase/auth";

const userAuthContext = createContext();
// Initialize Firebase Authentication and get a reference to the service

export function UserAuthContextProvider({ children }) {
  const [user, setUser] = useState({});

  function logIn(email, password) {
    //return signInWithEmailAndPassword(auth, email, password);
  }
  function signUp(email, password) {
    //return createUserWithEmailAndPassword(auth, email, password);
  }
  function logOut() {
    //return signOut(auth);
  }

  function onAuthStateChanged() {

  }
  /*
  useEffect(() => {
    
    const unsubscribe = onAuthStateChanged(auth, (currentuser) => {
      console.log("Auth", currentuser);
      setUser(currentuser);
    });

    return () => {
      unsubscribe();
    };
  }, []);
  */

  return (
    <userAuthContext.Provider
      value={{ user, logIn, signUp, logOut }}
    >
      {children}
    </userAuthContext.Provider>
  );
}

export function useUserAuth() {
  return useContext(userAuthContext);
}