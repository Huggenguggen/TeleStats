export const useFileRef = () => {
  return useState("fileRef", () => {})
}
export const useFilename = () => {
  return useState("filename", () => '')
}
export const useSelected = () => {
  return useState("selected", () => [])
}