
import { FaBars, FaAngleDown } from 'react-icons/fa';
import React, { useState, useRef } from "react";
import Link from "next/link";
import LogoIcon from "@/app/images/logos_transparent.png";
import LogoWhite from "@/app/images/logos_white.png";
import Image from "next/image";
import { useTheme } from 'next-themes';

type NavbarProps = {
    onNavClick: (sectionName: string) => void;
}

const style = {
    main: "fixed top-0 left-0 w-full h-12 z-20 mt-6",
    container: "container mx-auto px-4 sm:px-6 md:px-8 h-full gap-x-[2rem] flex flex-col justify-between items-center",
    logowrap: "h-full px-16 text-2xl rounded-full flex flex-row items-center bg-[#e23832] hover:bg-opacity-80 backdrop-blur-lg drop-shadow-lg",
}

const Navbar = ({ onNavClick }: NavbarProps) => {
    return (
        <>
            <div className={style.main}>
                <div className={style.container}>
                    <div className={style.logowrap}>
                        <div>
                            PoemGen
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

export default Navbar;    