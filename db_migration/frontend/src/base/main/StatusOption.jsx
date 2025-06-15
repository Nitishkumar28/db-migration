import useUIStore from "../../store/uistore"
import { header_sizes, header_weight } from "../Base";
import { themePalette } from "../colorPalette";

const StatusOption = ({text, status}) => {
    const activeTheme = useUIStore(state => state.theme);
    const greenLight = <i style={{color: themePalette[activeTheme].success, fontSize: header_sizes.extrasmall}} className="fa fa-circle"></i>
    const redLight = <i style={{color: themePalette[activeTheme].error, fontSize: header_sizes.extrasmall}} className="fa fa-circle"></i>
    const grayLight = <i style={{color: themePalette[activeTheme].pending, fontSize: header_sizes.extrasmall}} className="fa fa-circle"></i>
    const light = status === "connected" ? greenLight : status === "pending" ? grayLight : redLight;
    return (
        <span className={`capitalize ${header_weight.light}`}>{text} {light}</span>
    )
}

export default StatusOption;