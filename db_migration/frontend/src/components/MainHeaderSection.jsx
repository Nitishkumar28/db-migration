import { Header } from "../base/Base";

const MainHeaderSection = () => {
    return (
        <div className="flex flex-col justify-center items-center gap-1">
            <Header text="Fast & Flexible Migration Tool" size="large" weight="normal" />
            <Header text="(supports PostgreSQL, Oracle, and MySQL)" size="small" weight="light" />
        </div>
    )
}

export default MainHeaderSection;