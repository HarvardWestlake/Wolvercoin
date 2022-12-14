import React from 'react';
/**
 *  ImageUpload
 *
 *  Input Props:
 *  onUpdateImage :  function  to update parent state
 *  allowedSize   :   (optional) size to constrain upload
 *
 *  Usage:
 *  <ImageUpload onUpdate={this.updateImage} image={this.state.image} />
 *
 *  Notes:
 *  Default Allowed Size: 500000
 *
 *  Recommended Method:

   updateImage(imageUpload) {
     let imageBase64 = imageUpload.image;
     this.setState({imageBase64});
   }

 *
 */
const FILE_SIZE_MAX = 500000;
class ImageUpload extends React.Component {
  constructor(props) {
    super(props);
    this.handleFileRead = this.handleFileRead.bind(this);
    this.state = {
      imageBase64 : '',
      error : ''
    };

    this.allowedSize = FILE_SIZE_MAX;
    if (this.props.allowedSize && !isNaN(Number(this.props.allowedSize))) {
      this.allowedSize = this.props.allowedSize;
    }
  }

  handleFileRead = async (event) => {
    const file = event.target.files[0];
    var error = '';

    // Validate image is correct size and dimensions
    if (file.size > FILE_SIZE_MAX) {
      error += "File too large.  ";
    } else if (!file.type.startsWith('image/')){
      error += "File not an image.  File is " + file.type;
    }

    let finalFile = file;
    let imageBase64 = await this.convertBase64(file);

    // Validate image is correct size and dimensions
    if (file.size > FILE_SIZE_MAX) {
      error += "File too large.  ";
    } else if (!file.type.startsWith('image/')){
      error += "File not an image.  File is " + file.type;
    }

    if (error === '') {
      await this.setState({
        error : error,
        file : file,
        imageBase64, imageBase64
      });
      await this.props.onUpdate(imageBase64, file);
    } else {
      await this.setState({error});
    }
  }

  convertBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file)
      fileReader.onload = () => {
        resolve(fileReader.result);
      }
      fileReader.onerror = (error) => {
        reject(error);
      }
    })
  }

  renderError(error) {
     if (error === '') {
       return (<div></div>);
     }
     return (<div className="error"><b>{error}</b></div>);
  }

  render() {
    let msg = this.state.imageBase64 ? "Image Selected:" : "Choose an Image:";
    let errorHidden = this.renderError(this.state.error);
    return (
      <div key="imageUpload">
        <div>{msg}   {errorHidden}</div>
        <input id="inp" type="file"  onChange={e => this.handleFileRead(e)} ></input>
        <p id="b64"></p>
        <img id="img" height="150" alt="" src={this.state.imageBase64}/>
      </div>
    );
  }
}
 export default ImageUpload;