import { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { getUserImagesThunk } from "../../../store/images";
import ImageCard from "../ImagesCard";

import "./ManageImagesIndex.css";

const ManageImagesIndex = () => {
    const dispatch = useDispatch();
    let images = useSelector((state) => state.images.userImages);
    const user = useSelector((state) => state.session.user);

    useEffect(() => {
        const imageRestore = async () => {
            await dispatch(getUserImagesThunk());
        };
        imageRestore();
    }, [dispatch]);

    if (!images) return null;

    images = Object.values(images)

    images?.sort(
        (a, b) => Date.parse(b.updated_at) - Date.parse(a.updated_at)
    );

    return (
        <>
            <div>
                {images.map((image) => {
                    return (
                        <ImageCard
                            image={image}
                            key={image.id}
                        />
                    );
                })}
            </div>
        </>
    );
};

export default ManageImagesIndex;
