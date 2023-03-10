import React from "react";
import { NavLink, Link } from "react-router-dom";
import { useSelector } from "react-redux";
import ProfileButton from "./ProfileButton";
import "./Navigation.css";
import logo from "../../assets/platepal.png";

import SearchBar from "../SearchBar";

function Navigation({ isLoaded }) {
  const sessionUser = useSelector((state) => state.session.user);

  return (
    <nav className="navbar">
      <ul className="navbar-content">
        <li className="nav-left-logo">
          <NavLink exact to="/">
            <img className="logo-image" src={logo} alt="logo"></img>
          </NavLink>
        </li>
        <li className="nav-search-bar">
          <SearchBar />
        </li>
        {isLoaded && sessionUser ? (
          <div className="nav-right-container">
            <li>
              <NavLink exact to="/businesses/new">
                Add a Business
              </NavLink>
            </li>
            <li>
              {/* path needs to be updated,
                  manual input of 1
                  needs to go to page with suggested businesses for user to review
              */}
              <NavLink exact to="/businesses/1/reviews/new">
                Write a Review
              </NavLink>
            </li>
            <li className="nav-right-login">
              <ProfileButton className="profile-button" user={sessionUser} />
            </li>
          </div>
        ) : (
          <>
            <Link to="/login">
              <button>
                Log In
              </button>
            </Link>

            <Link to="/signup">
              <button>
                Sign Up
              </button>
            </Link>
          </>
        )}
      </ul>
    </nav>
  );
}

export default Navigation;
