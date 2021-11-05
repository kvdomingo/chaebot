import React, { useState, useEffect } from "react";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  NavbarText,
  UncontrolledDropdown as Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
} from "reactstrap";
import { Image } from "cloudinary-react";
import { commands as menuItems } from "../commands/Content";
import axios from "axios";

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [version, setVersion] = useState("");

  useEffect(() => {
    axios
      .get("https://api.github.com/repos/kvdomingo/discord-kbot/tags", {
        headers: {
          Accept: "application/vnd.github.v3+json",
        },
      })
      .then(res => setVersion(res.data[0].name))
      .catch(err => console.error(err.message));
  }, []);

  function toggleNavbar() {
    setIsOpen(!isOpen);
  }

  return (
    <div>
      <Navbar color="light" light expand="lg">
        <NavbarBrand href="/">
          <Image
            cloudName="kdphotography-assets"
            className="img-fluid"
            publicId="kvisualbot/avatar"
            secure
            aspectRatio="1"
            radius="max"
            crop="fill"
            gravity="face"
            height={60}
          />
        </NavbarBrand>
        <NavbarText className="mr-3">
          <NavLink href="/">KVISUALBOT</NavLink>
        </NavbarText>
        <NavbarToggler onClick={toggleNavbar} />
        <Collapse isOpen={isOpen} navbar>
          <Nav navbar>
            <NavItem>
              <Dropdown nav inNavbar>
                <DropdownToggle nav caret>
                  Commands
                </DropdownToggle>
                <DropdownMenu right>
                  {menuItems.map(({ header }, i) => (
                    <DropdownItem key={i}>
                      <NavLink href={`#${header.toLowerCase()}`}>{header}</NavLink>
                    </DropdownItem>
                  ))}
                </DropdownMenu>
              </Dropdown>
            </NavItem>
          </Nav>
          <Nav className="ml-auto" navbar>
            <NavItem className="mx-1">
              <a
                href="https://discord.com/api/oauth2/authorize?client_id=726835246892580865&permissions=256064&scope=bot"
                className="btn btn-outline-primary"
                target="_blank"
                rel="noopener noreferrer"
              >
                Add to Discord
              </a>
            </NavItem>
            <NavItem className="mx-1">
              <a
                href="https://discord.gg/jQ5dpeN"
                className="btn btn-outline-success"
                target="_blank"
                rel="noopener noreferrer"
              >
                Join Discord server
              </a>
            </NavItem>
            <NavItem className="mx-1">
              <a
                href="https://github.com/kvdomingo/discord-kbot"
                className="btn btn-outline-secondary"
                target="_blank"
                rel="noopener noreferrer"
              >
                GitHub
              </a>
            </NavItem>
            <NavItem className="mx-3">
              <div className="text-muted text-monospace">{version}</div>
            </NavItem>
          </Nav>
        </Collapse>
      </Navbar>
    </div>
  );
}
