import { Header } from "../base/Base";

const MainHeaderSection = () => {
    return (
        <div className="flex flex-col justify-center items-center">
            <Header text="Fast & Flexible Migration Tool" size="medium" weight="normal" />
            <Header text="(supports PostgreSQL, Oracle, and MySQL)" size="extrasmall" weight="light" />
        </div>
    )
}

export default MainHeaderSection;