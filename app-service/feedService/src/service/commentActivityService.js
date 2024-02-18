let update = async (entity, info) => {
  try {
    Object.assign(entity, info);
    return entity.save();
  } catch (error) {
    throw error("Error:", error);
  }
};

const get = async (params = {}) => {
  try {
    let { condition = {}, projection = {}, options = {} } = params;
    return Models.CommentActivity.findOne(condition, projection, options);
  } catch (error) {
    console.error("Error:", error);
  }
};

const updatecomment = async (req, res, next) => {
  try {
    const { id } = req.params;
    const { user } = req.user;
    const data = req.body;
    let condition = { comment: id, user };
    let comment = await get({ condition });
    if (comment) {
      let result = await update(comment, data);
      return res.send({
        data: result,
        statusCode: STATUS_CODE.OK,
        status: MSG.DISPLAY_MSG,
      });
    }
    data.user = user;
    data.comment = id;
    let insertData = await new Models.CommentActivity(data).save();
    return res.send({
      data: insertData,
      statusCode: STATUS_CODE.OK,
      status: MSG.DISPLAY_MSG,
    });
  } catch (error) {
    return res.send({
      error: error.message,
      status: STATUS_CODE.INTERNAL_SERVER_ERROR,
    });
  }
};

module.exports = {
  updatecomment,
};
