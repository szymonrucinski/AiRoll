import React from 'react';
import { LazyLoadImage } from 'react-lazy-load-image-component';
import Spinner from 'react-spinner-material';

const spinner = () => {
    return <Spinner radius={120} color={"#333"} stroke={2} visible={true} />


}
const MyImage = (props: { link: string;}) => (
      <LazyLoadImage
       effect="blur"
      src={props.link}
      visibleByDefault={false}
      beforeLoad ={spinner}      
/>
);
 
export default MyImage;