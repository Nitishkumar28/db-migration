import { patchTestAPI, testAPI } from "../hooks/urls";
import { useFetch } from "../hooks/useFetch";
import { usePost } from "../hooks/usePost";
import { useUpdate } from "../hooks/useUpdate";

const Test = () => {
    const get_api = testAPI();
    const patch_api = patchTestAPI();

    const {update, data: update_response, updating, error} = useUpdate(get_api);
    const {post, data: post_response, posting, error: post_err} = usePost(get_api);
    const {data: fetched_data, loading, error: get_err} = useFetch(get_api);

    const handleGet = () => {
        console.log("Data fetched")
        console.log(fetched_data);
    }

    const handlePost = () => {
        console.log("Data Posted")
        const data = {
            "name": "ram chandra",
            "email": "ram@gmai.com",
            "phone": "8177366642"
        }
        post(data)
        console.log(post_response)
    }

    const handlePatch = () => {
        console.log("Data Patched")
        const data = {
            "id": 5,
            "email": "preethu@gmai.com"
        }
        update(data)
        console.log(update_response)
    }

    return (
        <div className="w-full h-full flex flex-col">
            <div className="border p-2 flex flex-col">
                <button onClick={() => handleGet()}>Get</button>
                {JSON.stringify(fetched_data)}
            </div>
            <div>
                <button onClick={() => handlePost()}>Post</button>
                {JSON.stringify(post_response)}
            </div>
            <div>
                <button onClick={() => handlePatch()}>update</button>
                {JSON.stringify(update_response)}
            </div>
        </div>
    )
}

export default Test;