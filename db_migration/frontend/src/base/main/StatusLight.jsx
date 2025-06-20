import useUIStore from "../../store/uistore"
import { header_sizes, header_weight } from "../Base";
import { themePalette } from "../colorPalette";

const StatusLight = ({text, status}) => {
    const { theme } = useUIStore();

    const greenLight = <i style={{color: themePalette[theme]?.success, fontSize: header_sizes.extrasmall}} className="fa fa-circle"></i>
    const redLight = <i style={{color: themePalette[theme]?.error, fontSize: header_sizes.extrasmall}} className="fa fa-circle"></i>
    const grayLight = <i style={{color: themePalette[theme]?.pending, fontSize: header_sizes.extrasmall}} className="fa fa-circle"></i>

    const light = status === "success" ? greenLight : status === "idle" ? grayLight : redLight;
    return (
        <span className={`capitalize ${header_weight.normal}`}>{text} {light}</span>
    )
}

export default StatusLight;